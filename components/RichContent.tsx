'use client'
import React from 'react'

function Table({text}:{text:string}){
 const lines=text.trim().split('\n').filter(Boolean)
 const rows=lines.filter(x=>x.includes('|')).map(x=>x.split('|').map(c=>c.trim()).filter(Boolean))
 const clean=rows.filter(r=>!r.every(c=>/^:?-+:?$/.test(c)))
 if(clean.length<2)return <p className="richPre">{text}</p>
 return <div className="tableWrap"><table className="richTable"><tbody>{clean.map((r,i)=><tr key={i}>{r.map((c,j)=>i===0?<th key={j}>{c}</th>:<td key={j}>{c}</td>)}</tr>)}</tbody></table></div>
}
export default function RichContent({text,svg,className=''}:{text?:string,svg?:string,className?:string}){
 const t=text||''
 const hasTable=t.split('\n').filter(x=>x.includes('|')).length>=2
 return <div className={className}>{hasTable?<Table text={t}/>:<div className="richText">{t}</div>}{svg&&<div className="figure" dangerouslySetInnerHTML={{__html:svg}}/>}</div>
}
