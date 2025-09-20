import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <section className="hero">
        <div className="container">
          <h1>Vibe Coding</h1>
          <p>Современная разработка с душой</p>
          <div className="hero-buttons">
            <Link to="/course" className="btn">
              Узнать о курсе
            </Link>
            <Link to="/topics" className="btn btn-secondary">
              Посмотреть темы
            </Link>
          </div>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2>Почему Vibe Coding?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🚀</div>
              <h3>Современные технологии</h3>
              <p>Изучайте самые актуальные инструменты и фреймворки в мире разработки</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💡</div>
              <h3>Практический подход</h3>
              <p>Создавайте реальные проекты и получайте опыт, который ценят работодатели</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Фокус на качестве</h3>
              <p>Учитесь писать не просто рабочий код, а код, который вдохновляет</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3>Командная работа</h3>
              <p>Развивайте навыки работы в команде и code review</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📈</div>
              <h3>Карьерный рост</h3>
              <p>Получите знания, которые помогут вам стать senior-разработчиком</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h3>Креативность</h3>
              <p>Развивайте творческое мышление и создавайте уникальные решения</p>
            </div>
          </div>
        </div>
      </section>

      <section className="stats">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">40+</div>
              <div className="stat-label">часов контента</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">5</div>
              <div className="stat-label">основных тем</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">8+</div>
              <div className="stat-label">практических заданий</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">100%</div>
              <div className="stat-label">практический подход</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
