import React, { useEffect, useState } from 'react'
import { Product } from '../interfaces/product'
import { Link } from 'react-router-dom'
import { REACT_APP_ADMIN_ENDPOINT, REACT_APP_MAIN_ENDPOINT } from '../constant'

const Main = () => {
  const [products, setProducts] = useState([] as Product[])

  useEffect(() => {
    ;(async () => {
      const response = await fetch(REACT_APP_ADMIN_ENDPOINT)
      const data = await response.json()
      setProducts(data)
    })()
  }, [])

  const like = async (id: number) => {
    await fetch(`${REACT_APP_MAIN_ENDPOINT}/${id}/like`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })

    setProducts(
      products.map((p: Product) => {
        if (p.id === id) {
          p.likes++
        }
        return p
      })
    )
  }

  return (
    <>
      {/* --- NAVBAR --- */}
      <nav className='navbar navbar-expand-lg navbar-dark bg-dark'>
        <div className='container'>
        <Link className='navbar-brand px-3 py-2' to='/'>
          ProductApp
        </Link>

          <div className='collapse navbar-collapse'>
            <ul className='navbar-nav ml-auto'>
              <li className='nav-item'>
                <Link className='nav-link' to='/admin/products'>
                  Products
                </Link>
              </li>
              <li className='nav-item'>
                <Link className='nav-link' to='/admin/products/create'>
                  Create Product
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* --- MAIN CONTENT --- */}
      <main role='main'>
        <div className='album py-5 bg-light'>
          <div className='container'>
            <div className='row'>
              {products.map((p: Product) => {
                return (
                  <div className='col-md-4' key={p.id}>
                    <div className='card mb-4 shadow-sm'>
                      <img src={p.image} height='180' alt='product_image' />
                      <div className='card-body'>
                        <p className='card-text'>{p.title}</p>
                        <div className='d-flex justify-content-between align-items-center'>
                          <div className='btn-group'>
                            <button
                              type='button'
                              className='btn btn-sm btn-outline-secondary'
                              onClick={() => like(p.id)}
                            >
                              Like
                            </button>
                          </div>
                          <small className='text-muted'>{p.likes} likes</small>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </main>
    </>
  )
}

export default Main
