
function updateDateTime() {
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const date = now.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' });
    
    document.getElementById('time').textContent = time;
    document.getElementById('date').textContent = date;
  
    
    const hour = now.getHours();
    let greeting = "Good Morning";
    if (hour >= 12 && hour < 18) greeting = "Good Afternoon";
    else if (hour >= 18) greeting = "Good Evening";
    document.getElementById('greeting').textContent = greeting;
  }
  
  
  function login() {
    alert("will be available soon");
  }
  
  function signup() {
    alert("Will available sson");
  }
  
  document.addEventListener('DOMContentLoaded', updateDateTime);
  
