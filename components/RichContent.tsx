'use client'
import React from 'react'

function Inline({text}:{text:string}){
 const parts=text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g).filter(Boolean)
 return <>{parts.map((p,i)=>{
   if(p.startsWith('**')&&p.endsWith('**'))return <strong key={i}>{p.slice(2,-2)}</strong>
   if(p.startsWith('*')&&p.endsWith('*'))return <em key={i}>{p.slice(1,-1)}</em>
   return <React.Fragment key={i}>{p}</React.Fragment>
 })}</>
}
function Table({lines}:{lines:string[]}){
 const rows=lines.map(x=>x.split('|').map(c=>c.trim()).filter(Boolean))
 const clean=rows.filter(r=>!r.every(c=>/^:?-+:?$/.test(c)))
 if(clean.length<2)return <p className="richPre">{lines.join('\n')}</p>
 return <div className="tableWrap"><table className="richTable"><tbody>{clean.map((r,i)=><tr key={i}>{r.map((c,j)=>i===0?<th key={j}><Inline text={c}/></th>:<td key={j}><Inline text={c}/></td>)}</tr>)}</tbody></table></div>
}
function Blocks({text}:{text:string}){
 const lines=text.replace(/\r/g,'').split('\n')
 const out:React.ReactNode[]=[]
 let i=0
 while(i<lines.length){
   const raw=lines[i], line=raw.trim()
   if(!line){i++;continue}
   if(line.includes('|') && i+1<lines.length && lines[i+1].includes('|')){
     const table:string[]=[]
     while(i<lines.length && lines[i].includes('|')){table.push(lines[i]);i++}
     out.push(<Table key={'t'+i} lines={table}/>)
     continue
   }
   if(line.startsWith('### ')){out.push(<h4 className="richH3" key={i}><Inline text={line.slice(4)}/></h4>);i++;continue}
   if(line.startsWith('## ')){out.push(<h3 className="richH2" key={i}><Inline text={line.slice(3)}/></h3>);i++;continue}
   if(line.startsWith('# ')){out.push(<h2 className="richH1" key={i}><Inline text={line.slice(2)}/></h2>);i++;continue}
   if(line.startsWith('> ')){out.push(<div className="richCallout" key={i}><Inline text={line.slice(2)}/></div>);i++;continue}
   if(/^[-*] /.test(line)){
     const items:string[]=[]
     while(i<lines.length && /^\s*[-*] /.test(lines[i])){items.push(lines[i].trim().slice(2));i++}
     out.push(<ul className="richList" key={'u'+i}>{items.map((x,j)=><li key={j}><Inline text={x}/></li>)}</ul>)
     continue
   }
   const para=[line];i++
   while(i<lines.length){
     const n=lines[i].trim()
     if(!n||/^#{1,3} /.test(n)||n.startsWith('> ')||/^[-*] /.test(n)||n.includes('|'))break
     para.push(n);i++
   }
   out.push(<p className="richParagraph" key={'p'+i}><Inline text={para.join(' ')}/></p>)
 }
 return <div className="richBlocks">{out}</div>
}
export default function RichContent({text,svg,className=''}:{text?:string,svg?:string,className?:string}){
 return <div className={className}><Blocks text={text||''}/>{svg&&<div className="figure" dangerouslySetInnerHTML={{__html:svg}}/>}</div>
}
