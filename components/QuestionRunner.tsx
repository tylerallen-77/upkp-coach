'use client'
import {useEffect,useMemo,useRef,useState} from 'react'
import {api} from '../lib/api'
import RichContent from './RichContent'

type Q={token:string,id:string,bab:string,lv:number,difficulty_label?:string,item_signature?:string,stem:string,opts:string[],svg?:string,opt_svgs?:string[],waktu:number,skill?:string}
type Props={bundle:any,onDone:(pm:any)=>void}
export default function QuestionRunner({bundle,onDone}:Props){
 const [questions]=useState<Q[]>(bundle.questions||[]),[indices,setIndices]=useState<number[]>((bundle.questions||[]).map((_:any,i:number)=>i))
 const [i,setI]=useState(0),[pass,setPass]=useState(1),[deferred,setDeferred]=useState<number[]>([]),[selected,setSelected]=useState<number|null>(null)
 const [confidence,setConfidence]=useState(''),[changes,setChanges]=useState(0),[first,setFirst]=useState<number|null>(null),[feedback,setFeedback]=useState<any>(null),[busy,setBusy]=useState(false),[elapsed,setElapsed]=useState(0),[reported,setReported]=useState(false)
 const started=useRef(performance.now()); const current=questions[indices[i]]
 useEffect(()=>{started.current=performance.now();setElapsed(0);setSelected(null);setConfidence('');setChanges(0);setFirst(null);setFeedback(null);setReported(false)},[i,pass])
 useEffect(()=>{const x=setInterval(()=>setElapsed(performance.now()-started.current),200);return()=>clearInterval(x)},[i,pass])
 const isExam=bundle.mode==='tryout'
 async function finish(){setBusy(true);try{const d=await api('/api/session/close',{method:'POST',body:JSON.stringify({session_id:bundle.session.id})});onDone(d.postmortem)}finally{setBusy(false)}}
 function advance(){if(i+1<indices.length){setI(i+1);return}if(isExam&&deferred.length&&pass<3){setIndices([...deferred]);setDeferred([]);setPass(pass+1);setI(0);return}finish()}
 async function submit(skip=false){
   if(feedback){advance();return} if(selected===null&&!skip)return
   setBusy(true)
   try{
    const d=await api('/api/attempt',{method:'POST',body:JSON.stringify({question_token:current.token,selected,elapsed_ms:Math.round(elapsed),first_selection_ms:first,answer_changes:changes,confidence,skipped:skip,pass_number:pass,session_id:bundle.session.id})})
    if(skip&&isExam&&pass<3)setDeferred(x=>[...x,indices[i]])
    if(d.deferred_feedback){advance();return}
    setFeedback(d)
   }finally{setBusy(false)}
 }
 async function report(){if(!current.item_signature||reported)return;const reason=window.prompt('Laporkan soal: ambiguous / wrong_key / broken_figure / typo / too_easy / too_hard / other','ambiguous');if(!reason)return;try{await api('/api/report-question',{method:'POST',body:JSON.stringify({item_signature:current.item_signature,question_id:current.id,reason,detail:''})});setReported(true)}catch(e:any){window.alert(e.message)}}
 function pick(x:number){if(feedback||busy)return;if(selected!==null&&selected!==x)setChanges(c=>c+1);setSelected(x);if(first===null)setFirst(Math.round(performance.now()-started.current))}
 if(!current)return <div className="panel">Menyiapkan sesi…</div>
 return <div className="runnerGrid">
   <section className="panel questionPanel">
    <div className="questionTop"><div className="tags"><span>{current.bab}</span><span>{current.difficulty_label||('L'+current.lv)}</span>{isExam&&<span>Pass {pass}</span>}</div><b className="timer">{Math.floor(elapsed/60000).toString().padStart(2,'0')}:{Math.floor((elapsed%60000)/1000).toString().padStart(2,'0')}</b></div>
    <div className="eyebrow">SOAL {i+1}/{indices.length} · TARGET {current.waktu}s</div>
    <RichContent text={current.stem} svg={current.svg} className="stem"/>
    <div className="options">{current.opts.map((o,idx)=><button key={idx} className={'option '+(selected===idx?'selected ':'')+(feedback&&feedback.answer===idx?'correct ':'')+(feedback&&selected===idx&&!feedback.correct?'wrong ':'')} onClick={()=>pick(idx)}>
      <b>{'ABCDE'[idx]}</b>{current.opt_svgs?.[idx]?<span className="optSvg" dangerouslySetInnerHTML={{__html:current.opt_svgs[idx]}}/>:<span>{o}</span>}
    </button>)}</div>
    {feedback&&<div className={'feedback '+(feedback.correct?'ok':'no')}><strong>{feedback.correct?'Benar':'Belum tepat'}</strong><RichContent text={feedback.explanation}/>{feedback.shortcut&&<p><b>⚡ Jalan cepat:</b> {feedback.shortcut}</p>}<button className="reportBtn" onClick={report} disabled={reported}>{reported?'✓ Laporan terkirim':'⚑ Laporkan soal ini'}</button></div>}
    <div className="runnerActions">{!feedback&&<button className="btn ghost" onClick={()=>submit(true)} disabled={busy}>{isExam?'Parkir ke pass berikutnya':'Lewati'}</button>}<button className="btn primary" disabled={busy||(selected===null&&!feedback)} onClick={()=>feedback?advance():submit(false)}>{busy?'Menyimpan…':feedback?'Lanjut →':'Jawab →'}</button></div>
   </section>
   <aside className="runnerSide"><div className="sideCard"><h4>Confidence</h4><div className="confidence">{['yakin','50:50','tebak'].map(x=><button className={confidence===x?'active':''} onClick={()=>setConfidence(x)} key={x}>{x}</button>)}</div></div><div className="sideCard"><h4>Coach</h4><p>{isExam?'Feedback ditahan sampai sesi selesai. Gunakan strategi multi-pass.':'Utamakan pola tercepat yang tetap dapat dipertanggungjawabkan.'}</p></div><div className="sideCard muted"><small>First selection</small><b>{first===null?'—':(first/1000).toFixed(1)+'s'}</b><small>Answer changes</small><b>{changes}</b></div></aside>
 </div>
}
