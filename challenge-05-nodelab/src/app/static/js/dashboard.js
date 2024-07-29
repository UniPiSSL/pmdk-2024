function openNotePopup() {
		
	if (window.location.pathname !== "/dashboard") {
		displayResponseBox({"error": "Η δημιουργία σημείωσης γίνεται μόνο από το /dashboard"})
	}

	const modal = document.getElementById("noteModal");
	const backdrop = document.getElementById("modalBackdrop");
		
	const main = document.getElementById("notesMain");
		
	modal.classList.remove("hidden");
	backdrop.classList.remove("hidden");
	main.classList.add("hidden");
}
	
function closeNotePopup() {
	const modal = document.getElementById("noteModal");
	const backdrop = document.getElementById("modalBackdrop");
	const main = document.getElementById("notesMain");
		
	modal.classList.add("hidden");
	backdrop.classList.add("hidden");
	main.classList.remove("hidden");
}

function showNote(json, type) {
	const notesDiv = document.getElementById("notesJson");
	const noteElement = document.createElement("div");
	noteElement.classList.add("userNote");
	
	const noteId = document.createElement("p");
	noteId.classList.add("note_show_id");

	const noteTitle = document.createElement("h3");

	const noteContent = document.createElement("p");

	const trashButton = document.createElement("button");
	trashButton.classList.add("trash-btn");

	const trashIcon = document.createElement("i");
	trashIcon.classList.add("fas", "fa-trash");
	
	if (type === "add") {
		noteId.textContent = "UUID Σημείωσης: " + json.addedNote.uuid;
		noteTitle.textContent = json.addedNote.title;
		noteContent.textContent = json.addedNote.content;
		trashButton.addEventListener("click", function() {
			deleteNote(json.addedNote.uuid);
		});  
	} else {
		noteId.textContent = "UUID Σημείωσης: " + json.uuid;
		noteTitle.textContent = json.title;
		noteContent.textContent = json.content;
		trashButton.addEventListener("click", function() {
			deleteNote(json.uuid);
		});  
	}

	trashButton.appendChild(trashIcon);

	noteElement.appendChild(noteTitle);
	noteElement.appendChild(noteContent);
	noteElement.appendChild(noteId);
	noteElement.appendChild(trashButton);

	notesDiv.appendChild(noteElement);
}

function submitNote() {

		const noteData = {
			title: document.getElementById("noteTitle").value,
			content: document.getElementById("noteInput").value
		};

		fetch("/api/note/add", {
				method: "POST",
				headers: {
						"Content-Type": "application/json"
				},
				body: JSON.stringify(noteData)
		})
		.then(response => response.json())
		.then(data => {
			if (data.error) {
				displayResponseBox(data);
			} else {
				closeNotePopup();
				showNote(data, "add");
				displayResponseBox(data);
			}
		})
		.catch(error => console.error("Error:", error));
}

function deleteNote(uuidNote) {
	const elements = document.querySelectorAll(".userNote");
	let parentDiv = null;

	elements.forEach(element => {
		const uuidElement = element.querySelector(".note_show_id");

		if (uuidElement.textContent.includes(uuidNote)) {
			parentDiv = element;
		}
	});

	if (parentDiv) {
		const json = {
			uuid: uuidNote
		};

		fetch("/api/note/delete", {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(json)
		})
		.then(response => response.json())
		.then(data => {
			if (data.error) {
				displayResponseBox(data);
			} else {
				parentDiv.remove();
				displayResponseBox(data);
			}
		})
		.catch(error => console.error("Error:", error));
	}
}


function fetchAndDisplayNotes() {
	fetch("/api/note/all")
		.then(response => response.json())
		.then(data => {
			data.notes.forEach(note => {
				showNote(note, "");
			});
		})
		.catch(error => console.error("Error fetching notes:", error));
}

document.getElementById("submitNoteBtn").addEventListener("click", function() {  
	submitNote();
});

document.addEventListener("DOMContentLoaded", () => {
	fetchAndDisplayNotes();
});

function updateUserInfo(event) {

	event.preventDefault();

	const form = event.target;
	const currentPassword = form.currentPassword.value;
	const newUsername = form.newUsername.value;
	const newSchool = form.newSchool.value;
	const newPassword = form.newPassword.value;

	const data = {
		currentPassword: currentPassword,
		updates: {}
	};

	if (newUsername.trim() !== "") {
		data.updates.username = newUsername;
	}
	if (newSchool.trim() !== "") {
		data.updates.school = newSchool;
	}
	if (newPassword.trim() !== "") {
		data.updates.password = newPassword;
	}

	fetch("/api/auth/update", {
			method: "PUT",
			headers: {
					"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
	})
	.then(response => response.json())
	.then(data => {
		displayResponseBox(data);
	})
	.catch(error => console.error("Error:", error));
}



function dashboard() {
	window.location.href = "/dashboard";
}

function logout() {
	fetch("/api/auth/logout")
		.then(response => {
			window.location.href = "/"; 
		})
}

function profile() {
		window.location.href = "/profile";
}
	
function admin() {
		window.location.href = "/administration";
}
