const messages = [
  '👋 Hello there!',
  '💡 We love tech that sticks with you!',
  '📩 Contact us → attach2tech@gmail.com',
  '🤝 Join us — let’s build the future together!'
];
let index = 0;
setInterval(() => {
  index = (index + 1) % messages.length;
  const bubble = document.getElementById('chatBubble');
  bubble.style.opacity = 0;
  setTimeout(() => {
    bubble.textContent = messages[index];
    bubble.style.opacity = 1;
  }, 500);
}, 4000);

function scrollToSection(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

document.querySelectorAll('nav a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = link.getAttribute('href').replace('#', '');
    scrollToSection(target);
  });
});


document.getElementById('quoteForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch('/submit_quote', {
    method: 'POST',
    body: formData
  });
  const result = await response.json();
  
  if (result.status === 'success') {
    alert('✅ ' + result.message);
    this.reset();
  } else {
    alert('⚠️ ' + result.message);
  }
});



async function generatePlan() {
  const idea = document.getElementById('quickIdea').value.trim();
  if (!idea) {
    alert("Please enter your idea first!");
    return;
  }

  const btn = document.querySelector('.quote button');
  btn.innerText = "Generating...";
  btn.disabled = true;

  const response = await fetch('/generate_plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idea })
  });

  const data = await response.json();
  const planDiv = document.getElementById('planResult');
  planDiv.innerHTML = "";

  const text = `
    💡 <strong>Project Type:</strong> ${data.project_type}<br>
    🧰 <strong>Recommended Tools:</strong> ${data.tools}<br>
    📦 <strong>Deliverables:</strong> ${data.deliverables}<br>
    💸 <strong>Estimated Cost:</strong> ${data.estimated_cost}<br>
    🔧 <strong>Maintenance Cost:</strong> ${data.maintenance_cost}<br>
    ⏱️ <strong>Timeline:</strong> ${data.timeline}<br>
    🤖 <strong>AI Insight:</strong> ${data.ai_tip}<br>
    💬 <strong>Extra Tip:</strong> ${data.bonus}
  `;

  // Typing effect
  let i = 0;
  const speed = 20;
  function typeWriter() {
    if (i < text.length) {
      planDiv.innerHTML = text.substring(0, i+1);
      i++;
      setTimeout(typeWriter, speed);
    } else {
      btn.innerText = "Generate Plan";
      btn.disabled = false;
    }
  }
  typeWriter();
}

document.getElementById('year').textContent = new Date().getFullYear();

