const API_BASE = location.protocol + '//' + location.hostname + ':443'; // proxy will route
let token = null;

async function register(){
  const username = document.getElementById('reg_user').value;
  const email = document.getElementById('reg_email').value;
  const password = document.getElementById('reg_pass').value;
  const res = await fetch(API_BASE + '/register', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({username, email, password})
  });
  alert((await res.json()).msg || JSON.stringify(await res.json()));
}

async function login(){
  const username = document.getElementById('login_user').value;
  const password = document.getElementById('login_pass').value;
  const res = await fetch(API_BASE + '/login', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({username, password})
  });
  const data = await res.json();
  if (data.access_token){
    token = data.access_token;
    document.getElementById('auth').style.display = 'none';
    document.getElementById('search_ui').style.display = 'block';
  } else {
    alert('login failed');
  }
}

async function doSearch(){
  const q = document.getElementById('q').value;
  const min_price = document.getElementById('min_price').value;
  const max_price = document.getElementById('max_price').value;
  const sort_by = document.getElementById('sort_by').value;
  const params = new URLSearchParams();
  if (q) params.append('q', q);
  if (min_price) params.append('min_price', min_price);
  if (max_price) params.append('max_price', max_price);
  if (sort_by) params.append('sort_by', sort_by);
  const res = await fetch(API_BASE + '/search?' + params.toString(), {
    headers: {'Authorization': 'Bearer ' + token}
  });
  const data = await res.json();
  const container = document.getElementById('results');
  container.innerHTML = '';
  data.results.forEach(r => {
    const div = document.createElement('div');
    div.className = 'result';
    div.innerHTML = `<strong>${r.name}</strong> — ${r.type || ''} — ${r.average_price ? r.average_price + '€' : ''}<br>${r.description || ''}`;
    container.appendChild(div);
  });
}