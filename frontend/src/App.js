import React, { useState } from 'react';

function App() {
  const [isActivated, setIsActivated] = useState(false);

  const toggleSystem = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/toggle', {
        method: 'POST',
      });
      const result = await response.json();
      setIsActivated(!isActivated)
      console.log(result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Motion Detection System</h1>
      <button onClick={toggleSystem}>
        {isActivated ? 'Bật hệ thống' : 'Tắt hệ thống'}
      </button>
    </div>
  );
}

export default App;
