class AgentUI {
    constructor() {
        this.apiBase = '/api';
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
        document.querySelectorAll('.nav-item[data-view]').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchView(item.dataset.view);
            });
        });
        
        document.getElementById('sendBtn').addEventListener('click', () => this.sendMessage());
        document.getElementById('chatInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        document.getElementById('chatInput').addEventListener('input', (e) => {
            e.target.style.height = 'auto';
            e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
        });
        
        document.querySelectorAll('.input-hints code').forEach(hint => {
            hint.addEventListener('click', () => {
                document.getElementById('chatInput').value = hint.textContent;
                document.getElementById('chatInput').focus();
            });
        });
        
        document.getElementById('clearChat').addEventListener('click', () => this.clearChat());
        document.getElementById('refreshBtn').addEventListener('click', () => this.refreshCurrentView());
        
        document.getElementById('addUserBtn').addEventListener('click', () => this.showUserModal());
        document.getElementById('closeModal').addEventListener('click', () => this.hideUserModal());
        document.getElementById('cancelModal').addEventListener('click', () => this.hideUserModal());
        document.getElementById('submitModal').addEventListener('click', () => this.submitUserForm());
        
        document.getElementById('statusFilter').addEventListener('change', () => {
            this.currentPage = 1;
            this.loadUsers();
        });
        
        document.getElementById('userSearch').addEventListener('input', 
            this.debounce(() => {
                this.currentPage = 1;
                this.loadUsers();
            }, 300)
        );
        
        document.querySelectorAll('.page-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (btn.dataset.page === 'prev' && this.currentPage > 1) {
                    this.currentPage--;
                    this.loadUsers();
                } else if (btn.dataset.page === 'next') {
                    this.currentPage++;
                    this.loadUsers();
                }
            });
        });
    }
    
    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            if (data.status === 'healthy') {
                document.querySelector('.status-dot').classList.add('online');
            }
        } catch (error) {
            document.querySelector('.status-dot').classList.remove('online');
            document.querySelector('.status-text').textContent = '连接失败';
        }
    }
    
    switchView(view) {
        document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
        document.querySelector(`.nav-item[data-view="${view}"]`).classList.add('active');
        
        document.querySelectorAll('.content-area').forEach(area => area.classList.add('hidden'));
        document.getElementById(`${view}View`).classList.remove('hidden');
        
        const titles = {
            chat: '对话交互',
            users: '用户管理',
            stats: '数据统计'
        };
        document.querySelector('.page-title').textContent = titles[view] || view;
        
        if (view === 'users') {
            this.loadUsers();
        } else if (view === 'stats') {
            this.loadStatistics();
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        if (!message) return;
        
        input.value = '';
        input.style.height = 'auto';
        
        this.addMessage(message, 'user');
        
        try {
            const response = await fetch(`${this.apiBase}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            
            this.addMessage(data.message, 'assistant', data.data);
        } catch (error) {
            this.addMessage('请求失败，请检查网络连接', 'assistant');
        }
    }
    
    addMessage(text, role, data = null) {
        const container = document.getElementById('chatMessages');
        const messageEl = document.createElement('div');
        messageEl.className = `message ${role}`;
        
        let contentText = text;
        if (data && data.users) {
            contentText += '\n\n';
            data.users.slice(0, 5).forEach(user => {
                contentText += `• ${user.username} (${user.email})\n`;
            });
            if (data.users.length > 5) {
                contentText += `... 还有 ${data.users.length - 5} 个用户`;
            }
        }
        
        contentText = contentText.replace(/\n/g, '<br>');
        
        const avatar = role === 'user' ? '👤' : '🤖';
        const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        
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
        const container = document.getElementById('chatMessages');
        container.innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-text">对话已清空，请输入新的指令。</div>
                    <div class="message-time">${new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </div>
        `;
    }
    
    async loadUsers() {
        const status = document.getElementById('statusFilter').value;
        const search = document.getElementById('userSearch').value;
        
        try {
            let url = `${this.apiBase}/users?page=${this.currentPage}&page_size=${this.pageSize}`;
            if (status) url += `&status=${status}`;
            
            const response = await fetch(url);
            const data = await response.json();
            
            this.renderUsers(data.users || []);
            document.getElementById('currentPage').textContent = this.currentPage;
            
        } catch (error) {
            this.showToast('加载用户列表失败', 'error');
        }
    }
    
    renderUsers(users) {
        const tbody = document.getElementById('usersTableBody');
        
        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="loading-text">暂无数据</td></tr>';
            return;
        }
        
        tbody.innerHTML = users.map(user => `
            <tr>
                <td><code style="font-size:12px">${user.user_id.substring(0, 8)}...</code></td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.phone || '-'}</td>
                <td><span class="status-badge ${user.status}">${this.getStatusText(user.status)}</span></td>
                <td>${this.formatTime(user.created_at)}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn" onclick="agentUI.editUser('${user.user_id}')">编辑</button>
                        <button class="action-btn danger" onclick="agentUI.deleteUser('${user.user_id}')">删除</button>
                    </div>
                </td>
            </tr>
        `).join('');
    }
    
    getStatusText(status) {
        const map = { active: '活跃', inactive: '未活跃', deleted: '已删除' };
        return map[status] || status;
    }
    
    formatTime(timestamp) {
        if (!timestamp) return '-';
        return new Date(timestamp * 1000).toLocaleDateString('zh-CN');
    }
    
    async editUser(userId) {
        try {
            const response = await fetch(`${this.apiBase}/users/${userId}`);
            const user = await response.json();
            
            this.editingUserId = userId;
            document.getElementById('modalTitle').textContent = '编辑用户';
            
            const form = document.getElementById('userForm');
            form.username.value = user.username;
            form.email.value = user.email;
            form.phone.value = user.phone || '';
            form.status.value = user.status;
            form.tags.value = (user.tags || []).join(', ');
            
            this.showUserModal();
        } catch (error) {
            this.showToast('获取用户信息失败', 'error');
        }
    }
    
    async deleteUser(userId) {
        if (!confirm('确定要删除此用户吗？')) return;
        
        try {
            const response = await fetch(`${this.apiBase}/users/${userId}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            
            if (data.success) {
                this.showToast('删除成功', 'success');
                this.loadUsers();
            } else {
                this.showToast(data.error || '删除失败', 'error');
            }
        } catch (error) {
            this.showToast('删除失败', 'error');
        }
    }
    
    showUserModal() {
        document.getElementById('userModal').classList.add('show');
    }
    
    hideUserModal() {
        document.getElementById('userModal').classList.remove('show');
        document.getElementById('userForm').reset();
        this.editingUserId = null;
        document.getElementById('modalTitle').textContent = '添加用户';
    }
    
    async submitUserForm() {
        const form = document.getElementById('userForm');
        const formData = new FormData(form);
        
        const userData = {
            username: formData.get('username'),
            email: formData.get('email'),
            phone: formData.get('phone') || null,
            status: formData.get('status'),
            tags: formData.get('tags') ? formData.get('tags').split(',').map(t => t.trim()).filter(t => t) : []
        };
        
        try {
            let response;
            if (this.editingUserId) {
                response = await fetch(`${this.apiBase}/users/${this.editingUserId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });
            } else {
                response = await fetch(`${this.apiBase}/users`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.showToast(this.editingUserId ? '更新成功' : '创建成功', 'success');
                this.hideUserModal();
                this.loadUsers();
            } else {
                this.showToast(data.error || '操作失败', 'error');
            }
        } catch (error) {
            this.showToast('操作失败', 'error');
        }
    }
    
    async loadStatistics() {
        try {
            const response = await fetch(`${this.apiBase}/users`);
            const data = await response.json();
            const users = data.users || [];
            
            const stats = {
                total: data.total || users.length,
                active: users.filter(u => u.status === 'active').length,
                inactive: users.filter(u => u.status === 'inactive').length,
                deleted: users.filter(u => u.status === 'deleted').length
            };
            
            document.getElementById('totalUsers').textContent = stats.total;
            document.getElementById('activeUsers').textContent = stats.active;
            document.getElementById('inactiveUsers').textContent = stats.inactive;
            document.getElementById('deletedUsers').textContent = stats.deleted;
            
            const maxCount = Math.max(stats.active, stats.inactive, stats.deleted, 1);
            
            document.querySelectorAll('.chart-bar').forEach(bar => {
                const status = bar.dataset.status;
                const count = stats[status] || 0;
                const percentage = (count / maxCount) * 100;
                
                bar.querySelector('.bar-fill').style.width = percentage + '%';
                bar.querySelector('.bar-value').textContent = count;
            });
            
        } catch (error) {
            this.showToast('加载统计数据失败', 'error');
        }
    }
    
    refreshCurrentView() {
        const activeView = document.querySelector('.content-area:not(.hidden)').id;
        if (activeView === 'usersView') {
            this.loadUsers();
        } else if (activeView === 'statsView') {
            this.loadStatistics();
        }
        this.showToast('已刷新', 'success');
    }
    
    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
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
}

const agentUI = new AgentUI();
