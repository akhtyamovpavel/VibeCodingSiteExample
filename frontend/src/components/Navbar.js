import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            Vibe Coding
          </Link>
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link 
                to="/" 
                className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
              >
                Главная
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/course" 
                className={`nav-link ${location.pathname === '/course' ? 'active' : ''}`}
              >
                О курсе
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/topics" 
                className={`nav-link ${location.pathname === '/topics' ? 'active' : ''}`}
              >
                Темы
              </Link>
            </li>
            <li className="nav-item">
              <Link 
                to="/assignments" 
                className={`nav-link ${location.pathname === '/assignments' ? 'active' : ''}`}
              >
                Задания
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
