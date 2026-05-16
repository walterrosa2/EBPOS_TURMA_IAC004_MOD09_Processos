import { BrowserRouter, Routes, Route } from 'react-router-dom'
import DashboardLayout from './components/layout/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Processos from './pages/Processos'
import ProcessoNovo from './pages/ProcessoNovo'
import ProcessoEditar from './pages/ProcessoEditar'
import ProcessoDetalhe from './pages/ProcessoDetalhe'
import FluxoEditor from './pages/FluxoEditor'
import Analises from './pages/Analises'
import AnaliseDetalhe from './pages/AnaliseDetalhe'
import Automacoes from './pages/Automacoes'
import NotFound from './pages/NotFound'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/processos" element={<Processos />} />
          <Route path="/processos/novo" element={<ProcessoNovo />} />
          <Route path="/processos/:id/editar" element={<ProcessoEditar />} />
          <Route path="/processos/:id" element={<ProcessoDetalhe />} />
          <Route path="/processos/:id/fluxo" element={<FluxoEditor />} />
          <Route path="/processos/:id/analises" element={<Analises />} />
          <Route path="/processos/:id/analises/:analiseId" element={<AnaliseDetalhe />} />
          <Route path="/processos/:id/automacoes" element={<Automacoes />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
