import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Assignments.css';

const Assignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [activeAssignment, setActiveAssignment] = useState(null);
  const [revealedHints, setRevealedHints] = useState(0);
  const [hints, setHints] = useState([]); // уже полученные подсказки
  const [isLoadingHint, setIsLoadingHint] = useState(false);
  const [noMoreHints, setNoMoreHints] = useState(false);

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const response = await axios.get('/api/assignments');
        setAssignments(response.data);
      } catch (err) {
        setError('Ошибка при загрузке заданий');
        console.error('Error fetching assignments:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAssignments();
  }, []);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await axios.get('/api/topics/course/1');
        setTopics(response.data);
      } catch (err) {
        console.error('Error fetching topics for filter:', err);
      }
    };

    fetchTopics();
  }, []);

  const filteredAssignments = selectedTopic === 'all' 
    ? assignments 
    : assignments.filter(assignment => assignment.topic_id === parseInt(selectedTopic));

  const getDifficultyColor = (level) => {
    switch (level) {
      case 'easy': return '#51cf66';
      case 'medium': return '#ffd43b';
      case 'hard': return '#ff6b6b';
      default: return '#667eea';
    }
  };

  const getDifficultyLabel = (level) => {
    switch (level) {
      case 'easy': return 'Легко';
      case 'medium': return 'Средне';
      case 'hard': return 'Сложно';
      default: return level;
    }
  };

  const getTopicName = (topicId) => {
    const topic = topics.find((item) => item.id === topicId);
    if (!topic) {
      return `Тема #${topicId}`;
    }
    const prefix = topic.order_index ? `${topic.order_index}. ` : '';
    return `${prefix}${topic.title}`;
  };

  const baseScore = 100;
  const penaltiesSum = hints.slice(0, revealedHints).reduce((sum, h) => sum + (h.penalty || 10), 0);
  const currentScore = Math.max(0, baseScore - penaltiesSum);
  const visibleHints = hints
    .slice(0, revealedHints)
    .sort((a, b) => a.order_index - b.order_index);
  const shouldShowFallbackHints = visibleHints.length === 0 && noMoreHints;

  const defaultVerification = [
    'Проект запускается без ошибок и предупреждений',
    'Функционал соответствует описанию задания',
    'Структура кода аккуратна, нет дублирования',
  ];

  const defaultCriteria = [
    { name: 'Корректность работы', weight: 40 },
    { name: 'Качество кода и архитектура', weight: 30 },
    { name: 'Пользовательский опыт и дизайн', weight: 20 },
    { name: 'Соблюдение инструкций', weight: 10 },
  ];

  const defaultHints = [
    'Разбейте задачу на маленькие подзадачи и решайте по очереди.',
    'Проверьте граничные случаи и обработку ошибок заранее.',
    'Посмотрите, можно ли переиспользовать существующие компоненты/функции.',
  ];

  const openDetails = async (assignment) => {
    setActiveAssignment(assignment);
    setRevealedHints(0);
    setIsDetailsOpen(true);
    setNoMoreHints(false);
    setHints([]);
  };

  const closeDetails = () => {
    setIsDetailsOpen(false);
    setActiveAssignment(null);
  };

  const revealNextHint = async () => {
    if (!activeAssignment || isLoadingHint || noMoreHints) return;
    const nextIndex = revealedHints; // 0-based order_index
    setIsLoadingHint(true);
    try {
      const { data } = await axios.get(`/api/assignments/${activeAssignment.id}/hints/${nextIndex}`);
      // добавляем, если ещё не добавлена
      setHints((prev) => {
        const exists = prev.some((h) => h.order_index === data.order_index);
        return exists ? prev : [...prev, data].sort((a, b) => a.order_index - b.order_index);
      });
      setRevealedHints((prev) => prev + 1);
    } catch (e) {
      // если подсказок больше нет — блокируем кнопку
      console.warn('Подсказка недоступна или закончились', e);
      setNoMoreHints(true);
    } finally {
      setIsLoadingHint(false);
    }
  };

  if (loading) {
    return <div className="loading">Загрузка заданий...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="assignments">
      <div className="page-header">
        <div className="container">
          <h1>Домашние задания</h1>
          <p>Практические задания для закрепления знаний</p>
        </div>
      </div>

      <div className="container">
        <div className="assignments-content">
          <div className="assignments-header">
            <h2>Все задания курса</h2>
            <div className="assignments-controls">
              <label htmlFor="topic-filter">Фильтр по теме</label>
              <select
                id="topic-filter"
                value={selectedTopic}
                onChange={(event) => setSelectedTopic(event.target.value)}
              >
                <option value="all">Все темы</option>
                {topics.map((topic) => (
                  <option key={topic.id} value={topic.id}>
                    {topic.order_index ? `${topic.order_index}. ` : ''}
                    {topic.title}
                  </option>
                ))}
              </select>
            </div>
            <div className="assignments-stats">
              <div className="stat">
                <span className="stat-number">{assignments.length}</span>
                <span className="stat-label">всего заданий</span>
              </div>
              <div className="stat">
                <span className="stat-number">
                  {assignments.filter(a => a.is_required).length}
                </span>
                <span className="stat-label">обязательных</span>
              </div>
              <div className="stat">
                <span className="stat-number">
                  {assignments.reduce((sum, a) => sum + a.estimated_hours, 0)}
                </span>
                <span className="stat-label">часов практики</span>
              </div>
            </div>
          </div>

          <div className="assignments-grid">
            {filteredAssignments.length > 0 ? (
              filteredAssignments.map((assignment) => (
                <div key={assignment.id} className="assignment-card">
                  <div className="assignment-header">
                    <h3>{assignment.title}</h3>
                    <div className="assignment-badges">
                      <span
                        className="difficulty"
                        style={{ backgroundColor: getDifficultyColor(assignment.difficulty_level) }}
                      >
                        {getDifficultyLabel(assignment.difficulty_level)}
                      </span>
                      <span className={assignment.is_required ? 'required' : 'optional'}>
                        {assignment.is_required ? 'Обязательное' : 'Дополнительное'}
                      </span>
                    </div>
                  </div>

                  <p className="assignment-description">{assignment.description}</p>

                  <div className="assignment-instructions">
                    <h4>Инструкции:</h4>
                    <div className="instructions-text">
                      {assignment.instructions.split('\n').map((instruction, index) => (
                        <p key={index}>{instruction.trim()}</p>
                      ))}
                    </div>
                  </div>

                  <div className="assignment-meta">
                    <div className="meta-item">
                      <span className="meta-icon">⏱️</span>
                      <span className="meta-text">{assignment.estimated_hours} часов</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-icon">📚</span>
                      <span className="meta-text">{getTopicName(assignment.topic_id)}</span>
                    </div>
                  </div>

                  <div className="assignment-actions">
                    <button className="btn btn-start">
                      Начать задание
                    </button>
                    <button className="btn btn-secondary" onClick={() => openDetails(assignment)}>
                      Подробнее
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="assignments-empty">
                <h3>Заданий для выбранной темы пока нет</h3>
                <p>Попробуйте выбрать другую тему или сбросить фильтр.</p>
              </div>
            )}
          </div>
        </div>
      </div>
      {isDetailsOpen && activeAssignment && (
        <div className="modal-overlay" onClick={closeDetails}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{activeAssignment.title}</h3>
              <button className="modal-close" onClick={closeDetails}>×</button>
            </div>
            <div className="modal-body">
              <section className="section">
                <h4>Проверка задания</h4>
                <ul className="checklist">
                  {(activeAssignment.verification || defaultVerification).map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </section>

              <section className="section">
                <h4>Критерии оценивания</h4>
                <div className="criteria">
                  {(activeAssignment.criteria || defaultCriteria).map((c, idx) => (
                    <div className="criterion" key={idx}>
                      <span className="criterion-name">{c.name}</span>
                      <span className="criterion-weight">{c.weight}%</span>
                    </div>
                  ))}
                </div>
              </section>

              <section className="section">
                <div className="hints-header">
                  <h4>Подсказки</h4>
                  <div className="score">Текущий балл: {currentScore} / {baseScore}</div>
                </div>
                <ul className="hints-list">
                  {visibleHints.length > 0 ? (
                    visibleHints.map((hint) => (
                      <li key={hint.order_index} className="hint revealed">
                        {hint.text}
                      </li>
                    ))
                  ) : shouldShowFallbackHints ? (
                    defaultHints.map((hint, idx) => (
                      <li key={`fallback-${idx}`} className="hint revealed fallback">
                        {hint}
                      </li>
                    ))
                  ) : (
                    <li className="hint hidden">Подсказки ещё не открыты.</li>
                  )}
                </ul>
                <button
                  className="btn btn-tertiary"
                  onClick={revealNextHint}
                  disabled={isLoadingHint || noMoreHints}
                >
                  {isLoadingHint
                    ? 'Загрузка...'
                    : noMoreHints
                      ? 'Подсказок больше нет'
                      : 'Показать подсказку (−10 баллов)'}
                </button>
              </section>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Assignments;
