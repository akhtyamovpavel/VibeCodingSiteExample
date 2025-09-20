import React, { useState, useEffect, useMemo } from 'react';
import { Link, useLocation, useParams } from 'react-router-dom';
import axios from 'axios';
import './CourseOverview.css';

const DIFFICULTY_LABELS = {
  beginner: 'Начальный уровень',
  intermediate: 'Средний уровень',
  advanced: 'Продвинутый уровень',
};

const CourseOverview = () => {
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();
  const { courseId: routeCourseId } = useParams();

  const resolvedCourseId = useMemo(() => {
    const parseId = (value) => {
      const numeric = Number(value);
      return Number.isInteger(numeric) && numeric > 0 ? numeric : null;
    };

    const fromRoute = parseId(routeCourseId);
    if (fromRoute) {
      return fromRoute;
    }

    const searchParams = new URLSearchParams(location.search);
    const fromQuery = parseId(searchParams.get('courseId'));
    if (fromQuery) {
      return fromQuery;
    }

    return 1;
  }, [location.search, routeCourseId]);

  useEffect(() => {
    const fetchCourse = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await axios.get(`/api/courses/${resolvedCourseId}`);
        setCourse(response.data);
      } catch (err) {
        const message =
          err?.response?.status === 404
            ? 'Курс не найден. Попробуйте выбрать другой курс на главной странице.'
            : 'Ошибка при загрузке информации о курсе';
        setError(message);
        console.error('Error fetching course:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, [resolvedCourseId]);

  if (loading) {
    return <div className="loading">Загрузка информации о курсе...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!course) {
    return <div className="error">Курс не найден</div>;
  }

  const difficultyKey =
    typeof course.difficulty_level === 'string'
      ? course.difficulty_level.toLowerCase()
      : 'beginner';
  const difficultyLabel = DIFFICULTY_LABELS[difficultyKey] || course.difficulty_level;
  const sortedTopics = [...(course.topics || [])].sort((a, b) => {
    if (a.order_index === b.order_index) {
      return a.id - b.id;
    }
    return a.order_index - b.order_index;
  });
  const descriptionParagraphs = (course.description
    ? course.description.split('\n')
    : ['Описание курса появится позже.'])
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  if (descriptionParagraphs.length === 0) {
    descriptionParagraphs.push('Описание курса появится позже.');
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
                {descriptionParagraphs.map((paragraph, index) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </div>
            </div>

            {sortedTopics.length > 0 && (
              <div className="topics-preview">
                <h2>Программа курса</h2>
                <ul className="topics-preview-list">
                  {sortedTopics.map((topic) => (
                    <li key={topic.id} className="topic-preview-item">
                      <span className="topic-order-badge">{topic.order_index}</span>
                      <div className="topic-preview-content">
                        <h3>{topic.title}</h3>
                        <p>{topic.description}</p>
                        <div className="topic-preview-meta">
                          <span>⏱️ {topic.duration_minutes} минут</span>
                          <span>📝 {topic.assignments?.length || 0} заданий</span>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

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
                  <div className="stat-value">{difficultyLabel}</div>
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
