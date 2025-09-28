/* frontend/src/App.jsx */
import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('AI算法');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('请先选择简历文件');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('category', category);
    try {
      const res = await fetch('http://demo02.2brain.ai/upload_resume', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || '上传失败');
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="header">
        <div className="logo">
          <span className="logo-icon">📋</span>
          <h1 className="title">Resume Doctor</h1>
        </div>
        <p className="subtitle">AI 智能简历诊断与岗位匹配</p>
      </div>

      <div className="main-container">
        <div className="upload-section">
          <div className="card upload-card">
            <div className="card-header">
              <h2>📄 上传简历</h2>
              <p>选择您的简历文件，我们将为您提供专业的诊断建议</p>
            </div>

            <div 
              className={`upload-area ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={e => setFile(e.target.files[0])}
                id="file-input"
              />
              <label htmlFor="file-input" className="upload-label">
                {file ? (
                  <div className="file-info">
                    <span className="file-icon">📄</span>
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">({(file.size / 1024).toFixed(1)} KB)</span>
                  </div>
                ) : (
                  <div className="upload-placeholder">
                    <span className="upload-icon">📁</span>
                    <span className="upload-text">点击或拖拽上传简历</span>
                    <span className="upload-hint">支持 PDF, TXT 格式</span>
                  </div>
                )}
              </label>
            </div>

            <div className="category-section">
              <label className="category-label">
                <span className="label-icon">🎯</span>
                选择目标职位方向
              </label>
              <select 
                value={category} 
                onChange={e => setCategory(e.target.value)}
                className="category-select"
              >
                <option value="AI算法">🤖 AI 算法</option>
                <option value="前端开发">💻 前端开发</option>
                <option value="产品运营">📊 产品运营</option>
                <option value="数据分析">📈 数据分析</option>
              </select>
            </div>

            <button 
              className={`upload-btn ${loading ? 'loading' : ''}`} 
              onClick={handleUpload} 
              disabled={loading || !file}
            >
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  正在分析中...
                </>
              ) : (
                <>
                  <span className="btn-icon">🔍</span>
                  开始诊断分析
                </>
              )}
            </button>

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}
          </div>
        </div>

        {result && (
          <div className="result-section">
            <div className="card result-card">
              <div className="result-header">
                <h2>📊 诊断结果</h2>
                <div className="score-badge">
                  <span className="score-label">匹配度</span>
                  <span className="score-value">{result.score}</span>
                </div>
              </div>

              <div className="result-content">
   
		<div className="diagnosis-content">
  		  <div className="suggestion-block">
    		    <h4>🧠 OpenAI 建议</h4>
    		    <p>{result.suggestion || '暂无建议'}</p>
  		  </div>
  	      	  <div className="suggestion-block">
    		    <h4>📚 书生模型建议</h4>
    		    <p>{result.suggestion_shusheng || '暂无建议'}</p>
  		  </div>
		</div>


                <div className="jobs-section">
                  <h3>💼 推荐岗位</h3>
                  <div className="jobs-grid">
                    {result.jobs?.slice(0, 4).map((job, idx) => (
                      <div key={idx} className="job-card">
                        <div className="job-header">
                          <h4 className="job-title">{job.title}</h4>
                          <span className="job-location">📍 {job.location}</span>
                        </div>
                        <div className="job-skills">
                          <span className="skills-label">技能要求:</span>
                          <div className="skills-tags">
                            {job.skills?.map((skill, skillIdx) => (
                              <span key={skillIdx} className="skill-tag">{skill}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    )) || (
                      <div className="no-jobs">
                        <span>暂无推荐岗位</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <footer className="footer">
        <p>© 2025 Track-B: Resume Doctor - AI 智能简历诊断系统</p>
      </footer>
    </div>
  );
}

export default App;
