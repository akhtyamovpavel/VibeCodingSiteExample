import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import CourseOverview from './pages/CourseOverview';
import Topics from './pages/Topics';
import Assignments from './pages/Assignments';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/course" element={<CourseOverview />} />
            <Route path="/courses/:courseId" element={<CourseOverview />} />
            <Route path="/topics" element={<Topics />} />
            <Route path="/assignments" element={<Assignments />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
