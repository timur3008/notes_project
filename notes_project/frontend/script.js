const API = "http://127.0.0.1:8000/api";
let token = localStorage.getItem("access");

// ---------- АВТОРИЗАЦИЯ ----------
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    const res = await fetch(`${API}/user/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    if (res.ok) {
        const data = await res.json();
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        token = data.access;
        showNotes();
    } else {
        alert("Ошибка входа");
    }
});

// ---------- РЕГИСТРАЦИЯ ----------
document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("registerUsername").value;
    const email = document.getElementById("registerEmail").value;
    const password1 = document.getElementById("registerPassword1").value;
    const password2 = document.getElementById("registerPassword2").value;

    const res = await fetch(`${API}/user/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password1, password2 })
    });

    if (res.ok) {
        alert("Регистрация успешна! Теперь войдите.");
    } else {
        alert("Ошибка регистрации");
    }
});

// ---------- ЗАГРУЗКА ЗАМЕТОК ----------
async function loadNotes() {
    const res = await fetch(`${API}/notes/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) {
        alert("Ошибка загрузки заметок");
        return;
    }

    const notes = await res.json();
    const list = document.getElementById("notesList");
    list.innerHTML = "";
    notes.forEach(n => {
        const li = document.createElement("li");
        li.innerHTML = `<b>${n.title}</b>: ${n.text}
      <button onclick="editNote(${n.id}, '${n.title}', \`${n.text}\`)">✏️</button>
      <button onclick="deleteNote(${n.id})">🗑</button>`;
        list.appendChild(li);
    });
}

// ---------- СОЗДАНИЕ/РЕДАКТИРОВАНИЕ ----------
document.getElementById("noteForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("noteTitle").value;
    const text = document.getElementById("noteText").value;

    let url = `${API}/notes/create/`;
    let method = "POST";

    if (document.getElementById("noteForm").dataset.editing) {
        const id = document.getElementById("noteForm").dataset.editing;
        url = `${API}/notes/update/${id}/`;
        method = "PUT";
    }

    const res = await fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title, text })
    });

    if (res.ok) {
        document.getElementById("noteForm").reset();
        document.getElementById("noteForm").dataset.editing = "";
        document.getElementById("formTitle").innerText = "Создать заметку";
        loadNotes();
    } else {
        alert("Ошибка при сохранении");
    }
});

// ---------- УДАЛЕНИЕ ----------
async function deleteNote(id) {
    if (!confirm("Удалить заметку?")) return;
    await fetch(`${API}/notes/delete/${id}/`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });
    loadNotes();
}

// ---------- РЕДАКТИРОВАНИЕ ----------
function editNote(id, title, text) {
    document.getElementById("noteTitle").value = title;
    document.getElementById("noteText").value = text;
    document.getElementById("noteForm").dataset.editing = id;
    document.getElementById("formTitle").innerText = "Редактировать заметку";
}

// ---------- ВЫХОД ----------
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    token = null;
    document.getElementById("auth").style.display = "block";
    document.getElementById("notes").style.display = "none";
});

// ---------- ПЕРЕКЛЮЧЕНИЕ ----------
function showNotes() {
    document.getElementById("auth").style.display = "none";
    document.getElementById("notes").style.display = "block";
    loadNotes();
}

if (token) showNotes();
