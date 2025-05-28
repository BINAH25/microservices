import React from 'react'

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Products from './admin/Products'
import ProductsCreate from './admin/ProductsCreate'
import ProductsEdit from './admin/ProductsEdit'
import Main from './main/Main'

import './App.css'

function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route path='/' element={<Main />} />
          <Route path='/admin/products' element={<Products />} />
          <Route path='/admin/products/create' element={<ProductsCreate />} />
          <Route path='/admin/products/:id/edit' element={<ProductsEdit />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
