import { HashRouter, Route, Routes } from "react-router-dom"
import { Home } from "./pages/Home"
import { CreateProduct } from "./pages/CreateProduct"
import { Navbar } from "./components/Navbar"
import { InventoryProduct } from "./pages/InventoryProduct"

function App() {
  return (
    <HashRouter>
      <header>
          <Navbar/>
      </header>
      <main>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/create" element={<CreateProduct />} />
          <Route path="/inventory/:productId" element={<InventoryProduct />} />
        </Routes>
      </main>
    </HashRouter>

  )
}

export default App
