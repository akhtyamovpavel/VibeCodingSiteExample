import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Home.css';

const DIFFICULTY_LABELS = {
  beginner: 'Начальный уровень',
  intermediate: 'Средний уровень',
  advanced: 'Продвинутый уровень',
};

const Home = () => {
  const [courses, setCourses] = useState([]);
  const [loadingCourses, setLoadingCourses] = useState(true);
  const [coursesError, setCoursesError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const fetchCourses = async () => {
      try {
        const response = await axios.get('/api/courses/');
        if (!isMounted) return;
        setCourses(response.data);
      } catch (error) {
        if (!isMounted) return;
        setCoursesError('Не удалось загрузить список курсов. Попробуйте обновить страницу.');
        console.error('Error fetching courses:', error);
      } finally {
        if (isMounted) {
          setLoadingCourses(false);
        }
      }
    };

    fetchCourses();

    return () => {
      isMounted = false;
    };
  }, []);

  const getCourseDescriptionPreview = (description) => {
    if (!description) {
      return 'Описание курса появится позже.';
    }

    const normalized = description
      .split('\n')
      .map((paragraph) => paragraph.trim())
      .filter(Boolean);

    return normalized[0] || description.trim();
  };

  return (
    <div className="home">
      <section className="hero">
        <div className="container">
          <h1>Vibe Coding</h1>
          <p>Современная разработка с душой</p>
          <div className="hero-buttons">
            <Link to="/courses/1" className="btn">
              Узнать о курсе
            </Link>
            <Link to="/topics" className="btn btn-secondary">
              Посмотреть темы
            </Link>
          </div>
        </div>
      </section>

      <section className="course-showcase">
        <div className="container">
          <div className="section-header">
            <h2>Наши курсы</h2>
            <p>Выберите программу обучения и начните путь к новой карьере в разработке.</p>
          </div>

          {loadingCourses ? (
            <div className="course-loading">Загрузка курсов...</div>
          ) : coursesError ? (
            <div className="course-error">{coursesError}</div>
          ) : courses.length === 0 ? (
            <div className="course-empty">Пока что нет доступных курсов. Загляните позже!</div>
          ) : (
            <div className="course-grid">
              {courses.map((course) => {
                const difficulty =
                  typeof course.difficulty_level === 'string'
                    ? course.difficulty_level.toLowerCase()
                    : 'beginner';
                const difficultyLabel = DIFFICULTY_LABELS[difficulty] || course.difficulty_level;

                return (
                  <article key={course.id} className="course-card">
                    <div className="course-meta">
                      <span className="course-duration">⏱️ {course.duration_hours} часов</span>
                      <span className={`level-badge level-${difficulty}`}>{difficultyLabel}</span>
                    </div>
                    <h3>{course.title}</h3>
                    <p className="course-summary">{getCourseDescriptionPreview(course.description)}</p>
                    <div className="course-footer">
                      <Link to={`/courses/${course.id}`} className="btn btn-secondary">
                        Подробнее о курсе
                      </Link>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
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
