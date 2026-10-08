import './globals.css'
export const metadata={
  title:'UPKP Coach',
  description:'Adaptive learning coach untuk UPKP',
  applicationName:'UPKP Coach',
  icons:{icon:'/icon.svg'}
}
export const viewport={themeColor:'#0f1f3d'}
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="id"><body>{children}</body></html>}
