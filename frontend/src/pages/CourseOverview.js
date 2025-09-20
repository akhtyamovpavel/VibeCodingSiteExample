import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './CourseOverview.css';

const CourseOverview = () => {
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const response = await axios.get('/api/courses/1');
        setCourse(response.data);
      } catch (err) {
        setError('Ошибка при загрузке информации о курсе');
        console.error('Error fetching course:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, []);

  if (loading) {
    return <div className="loading">Загрузка информации о курсе...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!course) {
    return <div className="error">Курс не найден</div>;
  }

  return (
    <div className="course-overview">
      <div className="page-header">
        <div className="container">
          <h1>{course.title}</h1>
          <p>Погрузитесь в мир современной разработки</p>
        </div>
      </div>

      <div className="container">
        <div className="course-content">
          <div className="course-main">
            <div className="course-description">
              <h2>Описание курса</h2>
              <div className="description-text">
                {course.description.split('\n').map((paragraph, index) => (
                  <p key={index}>{paragraph.trim()}</p>
                ))}
              </div>
            </div>

            <div className="course-stats">
              <div className="stat-card">
                <div className="stat-icon">⏱️</div>
                <div className="stat-content">
                  <div className="stat-value">{course.duration_hours}</div>
                  <div className="stat-label">часов контента</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📚</div>
                <div className="stat-content">
                  <div className="stat-value">{course.topics?.length || 0}</div>
                  <div className="stat-label">тем для изучения</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🎯</div>
                <div className="stat-content">
                  <div className="stat-value">{course.difficulty_level}</div>
                  <div className="stat-label">уровень сложности</div>
                </div>
              </div>
            </div>
          </div>

          <div className="course-sidebar">
            <div className="sidebar-card">
              <h3>Что вы изучите</h3>
              <ul className="learning-list">
                <li>Современные технологии разработки</li>
                <li>Принципы чистой архитектуры</li>
                <li>Работу с базами данных</li>
                <li>Создание API и интеграции</li>
                <li>Лучшие практики разработки</li>
                <li>Командную работу и code review</li>
              </ul>
            </div>

            <div className="sidebar-card">
              <h3>Для кого этот курс</h3>
              <ul className="audience-list">
                <li>Начинающие разработчики</li>
                <li>Студенты IT-направлений</li>
                <li>Разработчики, желающие изучить новые технологии</li>
                <li>Все, кто хочет создавать качественные приложения</li>
              </ul>
            </div>

            <div className="sidebar-actions">
              <Link to="/topics" className="btn btn-full">
                Начать изучение
              </Link>
              <Link to="/assignments" className="btn btn-secondary btn-full">
                Посмотреть задания
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseOverview;
