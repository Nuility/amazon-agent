class AgentUI {
    constructor() {
        this.apiBase = "/api";
        this.currentPage = 1;
        this.pageSize = 20;
        this.editingUserId = null;

        this.init();
    }

    init() {
        this.bindEvents();
        this.checkHealth();
    }

    bindEvents() {
        document.querySelectorAll(".nav-item[data-view]").forEach((item) => {
            item.addEventListener("click", (e) => {
                e.preventDefault();
                this.switchView(item.dataset.view);
            });
        });

        document.getElementById("sendBtn").addEventListener("click", () => this.sendMessage());
        document.getElementById("chatInput").addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        document.getElementById("chatInput").addEventListener("input", (e) => {
            e.target.style.height = "auto";
            e.target.style.height = `${Math.min(e.target.scrollHeight, 120)}px`;
        });

        document.querySelectorAll(".input-hints code").forEach((hint) => {
            hint.addEventListener("click", () => {
                document.getElementById("chatInput").value = hint.textContent;
                document.getElementById("chatInput").focus();
            });
        });

        document.getElementById("clearChat").addEventListener("click", () => this.clearChat());
        document.getElementById("refreshBtn").addEventListener("click", () => this.refreshCurrentView());

        document.getElementById("addUserBtn").addEventListener("click", () => this.showUserModal());
        document.getElementById("closeModal").addEventListener("click", () => this.hideUserModal());
        document.getElementById("cancelModal").addEventListener("click", () => this.hideUserModal());
        document.getElementById("submitModal").addEventListener("click", () => this.submitUserForm());

        document.getElementById("statusFilter").addEventListener("change", () => {
            this.currentPage = 1;
            this.loadUsers();
        });

        document.getElementById("userSearch").addEventListener(
            "input",
            this.debounce(() => {
                this.currentPage = 1;
                this.loadUsers();
            }, 300)
        );

        document.querySelectorAll(".page-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                if (btn.dataset.page === "prev" && this.currentPage > 1) {
                    this.currentPage--;
                    this.loadUsers();
                } else if (btn.dataset.page === "next") {
                    this.currentPage++;
                    this.loadUsers();
                }
            });
        });

        const llmProvider = document.getElementById("llmProvider");
        if (llmProvider) {
            llmProvider.addEventListener("change", () => this.updateProviderUI());
        }

        const saveConfigBtn = document.getElementById("saveConfigBtn");
        if (saveConfigBtn) {
            saveConfigBtn.addEventListener("click", () => this.saveLLMConfig());
        }

        const testConnectionBtn = document.getElementById("testConnectionBtn");
        if (testConnectionBtn) {
            testConnectionBtn.addEventListener("click", () => this.testLLMConnection());
        }

        const runAgentBtn = document.getElementById("runAgentBtn");
        if (runAgentBtn) {
            runAgentBtn.addEventListener("click", () => this.runAgentWorkflow());
        }

        const reloadPromptBtn = document.getElementById("reloadPromptBtn");
        if (reloadPromptBtn) {
            reloadPromptBtn.addEventListener("click", () => this.loadPromptTemplate());
        }

        const savePromptBtn = document.getElementById("savePromptBtn");
        if (savePromptBtn) {
            savePromptBtn.addEventListener("click", () => this.savePromptTemplate());
        }
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            if (data.status === "healthy") {
                document.querySelector(".status-dot").classList.add("online");
                document.querySelector(".status-text").textContent = "Service online";
            }
        } catch (error) {
            document.querySelector(".status-dot").classList.remove("online");
            document.querySelector(".status-text").textContent = "Connection failed";
        }
    }

    switchView(view) {
        document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
        document.querySelector(`.nav-item[data-view="${view}"]`).classList.add("active");

        document.querySelectorAll(".content-area").forEach((area) => area.classList.add("hidden"));
        document.getElementById(`${this.getViewId(view)}View`).classList.remove("hidden");

        const titles = {
            chat: "Chat",
            users: "Users",
            stats: "Statistics",
            "llm-config": "LLM Settings",
            "agent-lab": "Agent Lab"
        };
        document.querySelector(".page-title").textContent = titles[view] || view;

        if (view === "users") {
            this.loadUsers();
        } else if (view === "stats") {
            this.loadStatistics();
        } else if (view === "llm-config") {
            this.loadLLMConfig();
        } else if (view === "agent-lab") {
            this.loadPromptTemplate();
        }
    }

    getViewId(view) {
        const viewMap = {
            "llm-config": "llmConfig",
            "agent-lab": "agentLab",
            chat: "chat",
            users: "users",
            stats: "stats"
        };
        return viewMap[view] || view;
    }

    async sendMessage() {
        const input = document.getElementById("chatInput");
        const message = input.value.trim();
        if (!message) return;

        input.value = "";
        input.style.height = "auto";

        this.addMessage(message, "user");

        try {
            const response = await fetch(`${this.apiBase}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            this.addMessage(data.message, "assistant", data.data);
        } catch (error) {
            this.addMessage("Request failed. Please check the server connection.", "assistant");
        }
    }

    addMessage(text, role, data = null) {
        const container = document.getElementById("chatMessages");
        const messageEl = document.createElement("div");
        messageEl.className = `message ${role}`;

        let contentText = text;
        if (data && data.users) {
            contentText += "\n\n";
            data.users.slice(0, 5).forEach((user) => {
                contentText += `- ${user.username} (${user.email})\n`;
            });
            if (data.users.length > 5) {
                contentText += `... and ${data.users.length - 5} more users`;
            }
        }

        if (data && data.statistics) {
            const stats = data.statistics;
            const active = stats.status_distribution?.active || 0;
            const inactive = stats.status_distribution?.inactive || 0;
            const deleted = stats.status_distribution?.deleted || 0;
            contentText += `\n\nActive: ${active}\nInactive: ${inactive}\nDeleted: ${deleted}`;
        }

        contentText = contentText.replace(/\n/g, "<br>");

        const avatar = role === "user" ? "U" : "AI";
        const time = new Date().toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });

        messageEl.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-text">${contentText}</div>
                <div class="message-time">${time}</div>
            </div>
        `;

        container.appendChild(messageEl);
        container.scrollTop = container.scrollHeight;
    }

    clearChat() {
        const container = document.getElementById("chatMessages");
        container.innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">AI</div>
                <div class="message-content">
                    <div class="message-text">Chat cleared. Enter a new command to continue.</div>
                    <div class="message-time">${new Date().toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}</div>
                </div>
            </div>
        `;
    }

    async loadUsers() {
        const status = document.getElementById("statusFilter").value;

        try {
            let url = `${this.apiBase}/users?page=${this.currentPage}&page_size=${this.pageSize}`;
            if (status) url += `&status=${status}`;

            const response = await fetch(url);
            const data = await response.json();

            this.renderUsers(data.users || []);
            document.getElementById("currentPage").textContent = this.currentPage;
        } catch (error) {
            this.showToast("Failed to load user list", "error");
        }
    }

    renderUsers(users) {
        const tbody = document.getElementById("usersTableBody");

        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-text">No users found</td></tr>';
            return;
        }

        tbody.innerHTML = users.map((user) => `
            <tr>
                <td><code style="font-size:12px">${user.user_id.substring(0, 8)}...</code></td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.phone || "-"}</td>
                <td><span class="status-badge ${user.status}">${this.getStatusText(user.status)}</span></td>
                <td>${this.formatTime(user.created_at)}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn" onclick="agentUI.editUser('${user.user_id}')">Edit</button>
                        <button class="action-btn danger" onclick="agentUI.deleteUser('${user.user_id}')">Delete</button>
                    </div>
                </td>
            </tr>
        `).join("");
    }

    getStatusText(status) {
        const map = { active: "Active", inactive: "Inactive", deleted: "Deleted" };
        return map[status] || status;
    }

    formatTime(timestamp) {
        if (!timestamp) return "-";
        return new Date(timestamp).toLocaleDateString("en-US");
    }

    async editUser(userId) {
        try {
            const response = await fetch(`${this.apiBase}/users/${userId}`);
            const user = await response.json();

            this.editingUserId = userId;
            document.getElementById("modalTitle").textContent = "Edit User";

            const form = document.getElementById("userForm");
            form.username.value = user.username;
            form.email.value = user.email;
            form.phone.value = user.phone || "";
            form.status.value = user.status;
            form.tags.value = (user.tags || []).join(", ");

            this.showUserModal();
        } catch (error) {
            this.showToast("Failed to load user details", "error");
        }
    }

    async deleteUser(userId) {
        if (!confirm("Delete this user?")) return;

        try {
            const response = await fetch(`${this.apiBase}/users/${userId}`, { method: "DELETE" });
            const data = await response.json();

            if (data.success) {
                this.showToast("User deleted", "success");
                this.loadUsers();
            } else {
                this.showToast(data.error || "Delete failed", "error");
            }
        } catch (error) {
            this.showToast("Delete failed", "error");
        }
    }

    showUserModal() {
        document.getElementById("userModal").classList.add("show");
    }

    hideUserModal() {
        document.getElementById("userModal").classList.remove("show");
        document.getElementById("userForm").reset();
        this.editingUserId = null;
        document.getElementById("modalTitle").textContent = "Add User";
    }

    async submitUserForm() {
        const form = document.getElementById("userForm");
        const formData = new FormData(form);

        const userData = {
            username: formData.get("username"),
            email: formData.get("email"),
            phone: formData.get("phone") || null,
            status: formData.get("status"),
            tags: formData.get("tags")
                ? formData.get("tags").split(",").map((tag) => tag.trim()).filter((tag) => tag)
                : []
        };

        try {
            let response;
            if (this.editingUserId) {
                response = await fetch(`${this.apiBase}/users/${this.editingUserId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData)
                });
            } else {
                response = await fetch(`${this.apiBase}/users`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(userData)
                });
            }

            const data = await response.json();

            if (data.success) {
                this.showToast(this.editingUserId ? "User updated" : "User created", "success");
                this.hideUserModal();
                this.loadUsers();
            } else {
                this.showToast(data.error || "Operation failed", "error");
            }
        } catch (error) {
            this.showToast("Operation failed", "error");
        }
    }

    async loadStatistics() {
        try {
            const response = await fetch(`${this.apiBase}/statistics`);
            const stats = await response.json();

            const totals = {
                total: stats.total_users || 0,
                active: stats.status_distribution?.active || 0,
                inactive: stats.status_distribution?.inactive || 0,
                deleted: stats.status_distribution?.deleted || 0
            };

            document.getElementById("totalUsers").textContent = totals.total;
            document.getElementById("activeUsers").textContent = totals.active;
            document.getElementById("inactiveUsers").textContent = totals.inactive;
            document.getElementById("deletedUsers").textContent = totals.deleted;

            const maxCount = Math.max(totals.active, totals.inactive, totals.deleted, 1);

            document.querySelectorAll(".chart-bar").forEach((bar) => {
                const status = bar.dataset.status;
                const count = totals[status] || 0;
                const percentage = (count / maxCount) * 100;

                bar.querySelector(".bar-fill").style.width = `${percentage}%`;
                bar.querySelector(".bar-value").textContent = count;
            });
        } catch (error) {
            this.showToast("Failed to load statistics", "error");
        }
    }

    refreshCurrentView() {
        const activeView = document.querySelector(".content-area:not(.hidden)").id;
        if (activeView === "usersView") {
            this.loadUsers();
        } else if (activeView === "statsView") {
            this.loadStatistics();
        }
        this.showToast("View refreshed", "success");
    }

    showToast(message, type = "info") {
        const container = document.getElementById("toastContainer");
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    debounce(func, wait) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    async loadLLMConfig() {
        try {
            const response = await fetch(`${this.apiBase}/config/llm`);
            const data = await response.json();

            const config = data.config || {};

            document.getElementById("llmEnabled").checked = data.enabled || false;

            const provider = config.provider || "mock";
            const providerSelect = document.getElementById("llmProvider");
            providerSelect.value = provider === "mock" ? "default" : provider;

            document.getElementById("llmApiKey").value = config.api_key || "";
            document.getElementById("llmApiEndpoint").value = config.api_endpoint || "";
            document.getElementById("llmModel").value = config.model || "";
            document.getElementById("llmTimeout").value = config.timeout || 30;
            document.getElementById("llmMaxRetries").value = config.max_retries || 3;

            this.updateProviderUI();
            this.updateStatusDisplay(data.enabled, provider);
        } catch (error) {
            this.showToast("Failed to load config", "error");
        }
    }

    updateProviderUI() {
        const provider = document.getElementById("llmProvider").value;
        const apiConfigCard = document.getElementById("apiConfigCard");
        const defaultModelInfo = document.getElementById("defaultModelInfo");
        const providerBadge = document.getElementById("providerBadge");

        const providerNames = {
            default: "Default",
            openai: "OpenAI",
            pangu: "Pangu",
            custom: "Custom API"
        };

        providerBadge.textContent = providerNames[provider] || provider;

        if (provider === "default") {
            defaultModelInfo.style.display = "block";
            apiConfigCard.style.display = "none";
        } else {
            defaultModelInfo.style.display = "none";
            apiConfigCard.style.display = "block";

            const hints = {
                openai: {
                    endpoint: "https://api.openai.com/v1",
                    model: "gpt-4.1 or gpt-4o-mini",
                    hint: "Paste an OpenAI API key"
                },
                pangu: {
                    endpoint: "Pangu endpoint URL",
                    model: "Pangu model name",
                    hint: "Paste a Pangu API key"
                },
                custom: {
                    endpoint: "Custom API base URL",
                    model: "Model identifier",
                    hint: "Paste your API key"
                }
            };

            const hint = hints[provider];
            if (hint) {
                document.getElementById("llmApiEndpoint").placeholder = hint.endpoint;
                document.getElementById("llmModel").placeholder = hint.model;
                document.getElementById("apiKeyHint").textContent = hint.hint;
            }
        }
    }

    updateStatusDisplay(enabled, provider) {
        const statusEl = document.getElementById("currentStatus");
        const providerEl = document.getElementById("currentProvider");

        statusEl.textContent = enabled ? "Enabled" : "Disabled";
        statusEl.style.color = enabled ? "#10b981" : "#ef4444";

        const providerNames = {
            mock: "Default mock client",
            openai: "OpenAI",
            pangu: "Pangu",
            custom: "Custom API"
        };
        providerEl.textContent = providerNames[provider] || provider;
    }

    async saveLLMConfig() {
        const provider = document.getElementById("llmProvider").value;
        const actualProvider = provider === "default" ? "mock" : provider;

        const config = {
            enabled: document.getElementById("llmEnabled").checked,
            provider: actualProvider,
            api_key: document.getElementById("llmApiKey").value,
            api_endpoint: document.getElementById("llmApiEndpoint").value,
            model: document.getElementById("llmModel").value,
            timeout: parseInt(document.getElementById("llmTimeout").value, 10) || 30,
            max_retries: parseInt(document.getElementById("llmMaxRetries").value, 10) || 3
        };

        if (config.enabled && provider !== "default" && !config.api_key) {
            this.showToast("API key is required", "error");
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/config/llm`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(config)
            });

            const data = await response.json();

            if (data.success) {
                this.showToast("Config saved", "success");
                this.updateStatusDisplay(config.enabled, actualProvider);
            } else {
                this.showToast(data.error || "Save failed", "error");
            }
        } catch (error) {
            this.showToast("Save failed", "error");
        }
    }

    async testLLMConnection() {
        const provider = document.getElementById("llmProvider").value;
        const actualProvider = provider === "default" ? "mock" : provider;

        const config = {
            enabled: true,
            provider: actualProvider,
            api_key: document.getElementById("llmApiKey").value,
            api_endpoint: document.getElementById("llmApiEndpoint").value,
            model: document.getElementById("llmModel").value,
            timeout: parseInt(document.getElementById("llmTimeout").value, 10) || 30,
            max_retries: parseInt(document.getElementById("llmMaxRetries").value, 10) || 3
        };

        try {
            this.showToast("Testing connection...", "info");

            const response = await fetch(`${this.apiBase}/config/llm/test`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(config)
            });

            const data = await response.json();

            if (data.success) {
                this.showToast(data.message || "Connection succeeded", "success");
            } else {
                this.showToast(data.error || "Connection failed", "error");
            }
        } catch (error) {
            this.showToast("Connection test failed", "error");
        }
    }

    async loadPromptTemplate() {
        try {
            const response = await fetch(`${this.apiBase}/ad-agent/prompt-template`);
            const data = await response.json();
            if (!data.success) {
                this.showToast(data.error || "Failed to load prompt template", "error");
                return;
            }

            const template = data.template;
            document.getElementById("promptSystemRole").value = template.system_role || "";
            document.getElementById("promptTaskTemplate").value = template.task_template || "";
            document.getElementById("promptOutputStyle").value = template.output_style || "";
        } catch (error) {
            this.showToast("Failed to load prompt template", "error");
        }
    }

    async savePromptTemplate() {
        const payload = {
            system_role: document.getElementById("promptSystemRole").value,
            task_template: document.getElementById("promptTaskTemplate").value,
            output_style: document.getElementById("promptOutputStyle").value
        };

        try {
            const response = await fetch(`${this.apiBase}/ad-agent/prompt-template`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (data.success) {
                this.showToast("Prompt template saved", "success");
            } else {
                this.showToast(data.error || "Failed to save prompt template", "error");
            }
        } catch (error) {
            this.showToast("Failed to save prompt template", "error");
        }
    }

    async runAgentWorkflow() {
        const objective = document.getElementById("agentObjective").value.trim();
        if (!objective) {
            this.showToast("Objective is required", "error");
            return;
        }

        try {
            this.showToast("Running agent workflow...", "info");
            const response = await fetch(`${this.apiBase}/ad-agent/run`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ objective })
            });
            const data = await response.json();

            if (!data.success) {
                this.showToast(data.error || "Agent run failed", "error");
                return;
            }

            this.renderAgentRun(data.run);
            this.showToast("Agent workflow completed", "success");
        } catch (error) {
            this.showToast("Agent run failed", "error");
        }
    }

    renderAgentRun(run) {
        document.getElementById("agentSteps").innerHTML = (run.steps || [])
            .map((step) => `<div><strong>${step.name}</strong> [${step.status}]<br>${step.detail}</div>`)
            .join("<hr>");

        document.getElementById("agentFindings").innerHTML = (run.findings || [])
            .map((item) => `- ${item}`)
            .join("<br>");

        document.getElementById("agentRecommendations").innerHTML = (run.recommendations || [])
            .map((item) => {
                return `<div><strong>${item.campaign_name}</strong><br>${item.reason}<br>${item.suggested_action}</div>`;
            })
            .join("<hr>");

        document.getElementById("agentPrompt").textContent = run.prompt || "";
        document.getElementById("agentLlmOutput").textContent = run.llm_output || "";
        document.getElementById("agentNextActions").innerHTML = (run.next_actions || [])
            .map((item) => `- ${item}`)
            .join("<br>");
    }
}

const agentUI = new AgentUI();
