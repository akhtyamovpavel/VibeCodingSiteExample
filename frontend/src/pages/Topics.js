import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Topics.css';

const Topics = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await axios.get('/api/topics/course/1');
        setTopics(response.data);
      } catch (err) {
        setError('Ошибка при загрузке тем курса');
        console.error('Error fetching topics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
  }, []);

  if (loading) {
    return <div className="loading">Загрузка тем курса...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="topics">
      <div className="page-header">
        <div className="container">
          <h1>Темы курса</h1>
          <p>Изучите все темы курса Vibe Coding</p>
        </div>
      </div>

      <div className="container">
        <div className="topics-grid">
          {topics.map((topic) => (
            <div key={topic.id} className="topic-card">
              <div className="topic-header">
                <div className="topic-order">{topic.order_index}</div>
                <h3>{topic.title}</h3>
              </div>
              
              <p className="topic-description">{topic.description}</p>
              
              <div className="topic-content">
                <h4>Содержание темы:</h4>
                <div className="content-text">
                  {topic.content.split('\n').map((paragraph, index) => (
                    <p key={index}>{paragraph.trim()}</p>
                  ))}
                </div>
              </div>
              
              <div className="topic-meta">
                <div className="duration">
                  ⏱️ {topic.duration_minutes} минут
                </div>
                <div className="assignments-count">
                  📝 {topic.assignments?.length || 0} заданий
                </div>
              </div>
              
              {topic.assignments && topic.assignments.length > 0 && (
                <div className="topic-assignments">
                  <h4>Задания по теме:</h4>
                  <ul className="assignments-list">
                    {topic.assignments.map((assignment) => (
                      <li key={assignment.id} className="assignment-item">
                        <Link to="/assignments" className="assignment-link">
                          {assignment.title}
                        </Link>
                        <span className={`difficulty ${assignment.difficulty_level}`}>
                          {assignment.difficulty_level}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Topics;
