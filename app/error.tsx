'use client'
export default function ErrorPage({reset}:{reset:()=>void}){return <main className="legal"><h1>Ada yang tidak beres.</h1><p>Progress yang sudah tersimpan tetap aman. Coba muat ulang halaman.</p><button onClick={()=>reset()}>Coba lagi</button> <a href="/">Kembali ke Beranda</a></main>}
