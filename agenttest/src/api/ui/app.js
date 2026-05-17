class AgentUI {
    constructor() {
        this.apiBase = "/api";
        this.currentPage = 1;
        this.pageSize = 20;
        this.editingUserId = null;
        this.currentView = "chat";
        this.currentLanguage = localStorage.getItem("agent-ui-language") || "zh";
        this.lastStats = null;
        this.lastUsers = [];
        this.lastLLMConfig = null;
        this.lastAgentRun = null;
        this.lastHealthState = "checking";
        this.objectiveTouched = false;
        this.languageOptions = [
            { code: "zh", label: "中文", badge: "中", locale: "zh-CN" },
            { code: "en", label: "English", badge: "EN", locale: "en-US" },
            { code: "es", label: "Español", badge: "ES", locale: "es-ES" },
            { code: "fr", label: "Français", badge: "FR", locale: "fr-FR" },
            { code: "de", label: "Deutsch", badge: "DE", locale: "de-DE" },
            { code: "pt", label: "Português", badge: "PT", locale: "pt-PT" },
            { code: "ja", label: "日本語", badge: "日", locale: "ja-JP" },
            { code: "ar", label: "العربية", badge: "ع", locale: "ar-SA" }
        ];
        this.translations = this.buildTranslations();
        this.init();
    }

    buildTranslations() {
        const en = {
            brandEyebrow: "Amazon Ads AI",
            brandTitle: "Agent Console",
            workspaceTitle: "Workspace",
            settingsTitle: "Settings",
            navChat: "Command Center",
            navChatHint: "Overview and guided chat",
            navUsers: "Entities",
            navUsersHint: "Users and operators",
            navStats: "Insights",
            navStatsHint: "Live metrics and charts",
            navAgentLab: "Agent Studio",
            navAgentLabHint: "Workflow and prompt design",
            navLlm: "LLM Setup",
            navLlmHint: "Provider and model settings",
            serviceStatusLabel: "Service status",
            statusPill: "Automation ready",
            topEyebrow: "Intelligent operations dashboard",
            clearChat: "Clear Chat",
            refresh: "Refresh",
            heroTag: "Amazon Ads Agent System",
            heroTitle: "From search term mining to campaign optimization in one workspace.",
            heroDesc: "Build an agent that can analyze search ads, recommend actions, optimize bidding strategy, and orchestrate prompt-driven workflows with a polished multilingual console.",
            heroPrimary: "Open Agent Studio",
            heroSecondary: "View Insight Board",
            heroVisualTitle: "Optimization signal",
            heroVisualTrend: "+18% efficiency",
            metricCtr: "CTR",
            metricAcos: "ACOS",
            metricRoas: "ROAS",
            overviewOneTitle: "Search Mining",
            overviewOneDesc: "Capture valuable search terms, isolate waste, and feed reusable insights into the recommendation loop.",
            overviewTwoTitle: "Auto Optimization",
            overviewTwoDesc: "Turn diagnostics into budget moves, bid tuning, negative keyword suggestions, and guardrail-backed actions.",
            overviewThreeTitle: "Prompt Workflow",
            overviewThreeDesc: "Design structured prompts and chain them into repeatable ad analysis workflows across teams.",
            chatPlaceholder: "Enter a command... Press Enter to send, Shift+Enter for a new line.",
            sendMessageAria: "Send message",
            languageSelectorAria: "Language selector",
            quickPrompts: "Quick prompts:",
            entityBannerEyebrow: "Operator data layer",
            entityBannerTitle: "Manage the people behind campaign decisions.",
            entityBannerMetricOne: "Active operators",
            entityBannerMetricTwo: "Workflow coverage",
            userSearchPlaceholder: "Search box reserved for future filtering",
            filterAllStatuses: "All statuses",
            addUser: "Add User",
            tableUserId: "User ID",
            tableUsername: "Username",
            tableEmail: "Email",
            tablePhone: "Phone",
            tableStatus: "Status",
            tableCreated: "Created",
            tableActions: "Actions",
            loadingUsers: "Loading users...",
            previous: "Previous",
            page: "Page",
            next: "Next",
            insightEyebrow: "Insight board",
            insightTitle: "A clearer picture of account health and workflow maturity.",
            insightSparklineLabel: "Workflow confidence trend",
            totalUsers: "Total Users",
            activeUsers: "Active Users",
            inactiveUsers: "Inactive Users",
            deletedUsers: "Deleted Users",
            statusDistribution: "Status Distribution",
            statusDistributionNote: "Synced from backend statistics",
            agentCoverageTitle: "Agent Coverage",
            agentCoverageNote: "Visual planning layer",
            donutCenterLabel: "Mapped",
            legendOne: "Analysis",
            legendTwo: "Optimization",
            legendThree: "Workflow",
            llmEyebrow: "Model operations",
            llmHeader: "LLM Configuration",
            llmDesc: "Configure the optional model provider used by the agent analysis features.",
            providerCardTitle: "Provider",
            enableLlm: "Enable LLM integration",
            providerLabel: "Provider",
            providerDefault: "Default mock client",
            providerCustom: "Custom API",
            providerBadgeDefault: "Default",
            apiSettingsTitle: "API Settings",
            apiKeyLabel: "API Key *",
            apiKeyPlaceholder: "Enter API key",
            apiKeyHint: "Paste your provider key here.",
            apiEndpointLabel: "API Endpoint",
            apiEndpointHint: "Leave blank to use the provider default if supported.",
            modelNameLabel: "Model Name",
            modelHint: "Set the model identifier used by your provider.",
            timeoutLabel: "Timeout (seconds)",
            retryLabel: "Max retries",
            defaultNotesTitle: "Default Client Notes",
            defaultNotesLead: "<strong>The default mock client</strong> is useful for local demos and UI testing.",
            defaultNoteOne: "No API key required",
            defaultNoteTwo: "Safe for local experimentation",
            defaultNoteThree: "Real providers are still optional in this project",
            testConnection: "Test Connection",
            saveConfig: "Save Config",
            configStatusLabel: "Status:",
            configProviderLabel: "Provider:",
            agentLabEyebrow: "Agent design system",
            agentLabHeader: "Agent Studio",
            agentLabDesc: "Prototype the ad analysis agent, workflow review loop, and prompt engineering surface in one place.",
            studioMetricOneLabel: "Analysis depth",
            studioMetricOneValue: "5 Layers",
            studioMetricTwoLabel: "Optimization scope",
            studioMetricTwoValue: "Bid / Budget / Query",
            studioMetricThreeLabel: "Prompt mode",
            studioMetricThreeValue: "Structured",
            runObjectiveTitle: "Run Objective",
            objectiveLabel: "Objective",
            objectiveDefault: "Improve campaign efficiency while protecting profitable growth.",
            runAgent: "Run Agent",
            promptTemplateTitle: "Prompt Template",
            systemRoleLabel: "System Role",
            taskTemplateLabel: "Task Template",
            outputStyleLabel: "Output Style",
            reloadTemplate: "Reload Template",
            saveTemplate: "Save Template",
            agentOutputTitle: "Agent Run Output",
            workflowSteps: "Workflow Steps",
            agentStepsEmpty: "Run the agent to inspect workflow steps.",
            findings: "Findings",
            findingsEmpty: "No findings yet.",
            recommendations: "Recommendations",
            recommendationsEmpty: "No recommendations yet.",
            promptPreview: "Prompt Preview",
            promptEmpty: "No prompt rendered yet.",
            llmOutput: "LLM Output",
            llmEmpty: "No model output yet.",
            nextActions: "Next Actions",
            nextActionsEmpty: "No next actions yet.",
            modalAddUser: "Add User",
            modalEditUser: "Edit User",
            fieldUsername: "Username *",
            fieldUsernamePlaceholder: "Enter username",
            fieldEmail: "Email *",
            fieldEmailPlaceholder: "Enter email",
            fieldPhone: "Phone",
            fieldPhonePlaceholder: "Enter phone number",
            fieldStatus: "Status",
            fieldTags: "Tags (comma separated)",
            fieldTagsPlaceholder: "ops, vip, trial",
            cancel: "Cancel",
            save: "Save",
            pageChat: "Command Center",
            pageUsers: "Entities",
            pageStats: "Insights",
            pageLlm: "LLM Setup",
            pageAgentLab: "Agent Studio",
            statusActive: "Active",
            statusInactive: "Inactive",
            statusDeleted: "Deleted",
            toastLoadUsersFailed: "Failed to load user list",
            toastLoadUserDetailsFailed: "Failed to load user details",
            toastDeleteConfirm: "Delete this user?",
            toastUserDeleted: "User deleted",
            toastDeleteFailed: "Delete failed",
            toastUserUpdated: "User updated",
            toastUserCreated: "User created",
            toastOperationFailed: "Operation failed",
            toastLoadStatisticsFailed: "Failed to load statistics",
            toastViewRefreshed: "View refreshed",
            toastLoadConfigFailed: "Failed to load config",
            toastApiKeyRequired: "API key is required",
            toastConfigSaved: "Config saved",
            toastSaveFailed: "Save failed",
            toastTestingConnection: "Testing connection...",
            toastConnectionSucceeded: "Connection succeeded",
            toastConnectionFailed: "Connection failed",
            toastConnectionTestFailed: "Connection test failed",
            toastLoadPromptFailed: "Failed to load prompt template",
            toastSavePromptFailed: "Failed to save prompt template",
            toastPromptSaved: "Prompt template saved",
            toastObjectiveRequired: "Objective is required",
            toastRunningAgent: "Running agent workflow...",
            toastAgentRunFailed: "Agent run failed",
            toastAgentCompleted: "Agent workflow completed",
            chatRequestFailed: "Request failed. Please check the server connection.",
            serviceOnline: "Service online",
            serviceOffline: "Connection failed",
            serviceChecking: "Checking...",
            welcomeTitle: "Welcome to the Amazon Ads agent workspace.",
            welcomeLineOne: "<strong>search term mining</strong> to inspect keyword opportunities",
            welcomeLineTwo: "<strong>query all users</strong> to view the current entity dataset",
            welcomeLineThree: "<strong>stats</strong> to check health metrics and distribution",
            welcomeLineFour: "<strong>help</strong> to review supported chat commands",
            welcomeFooter: "Use the left panels to move between entity management, metrics, model configuration, and prompt-driven agent workflows.",
            clearedChat: "Chat cleared. Enter a new command to continue.",
            noUsersFound: "No users found",
            defaultProviderName: "Default mock client",
            statusEnabled: "Enabled",
            statusDisabled: "Disabled",
            actionEdit: "Edit",
            actionDelete: "Delete",
            workflowStatusDone: "Done",
            workflowStatusRunning: "Running",
            workflowStatusPending: "Pending",
            openaiEndpointPlaceholder: "https://api.openai.com/v1",
            openaiModelPlaceholder: "gpt-4.1 or gpt-4o-mini",
            openaiApiHint: "Paste an OpenAI API key",
            panguEndpointPlaceholder: "Pangu endpoint URL",
            panguModelPlaceholder: "Pangu model name",
            panguApiHint: "Paste a Pangu API key",
            customEndpointPlaceholder: "Custom API base URL",
            customModelPlaceholder: "Model identifier",
            customApiHint: "Paste your API key"
        };

        const zh = {
            brandEyebrow: "亚马逊广告 AI",
            brandTitle: "智能体控制台",
            workspaceTitle: "工作台",
            settingsTitle: "配置中心",
            navChat: "指挥中心",
            navChatHint: "总览与对话入口",
            navUsers: "实体管理",
            navUsersHint: "用户与运营角色",
            navStats: "洞察看板",
            navStatsHint: "实时指标与图形",
            navAgentLab: "智能体工作室",
            navAgentLabHint: "工作流与 Prompt 设计",
            navLlm: "模型配置",
            navLlmHint: "服务商与模型参数",
            serviceStatusLabel: "服务状态",
            statusPill: "自动化已就绪",
            topEyebrow: "智能运营仪表台",
            clearChat: "清空对话",
            refresh: "刷新",
            heroTag: "Amazon Ads 智能体系统",
            heroTitle: "把搜索词挖掘、广告分析和自动优化放进同一套工作台。",
            heroDesc: "围绕亚马逊广告构建一个能做搜索广告分析、智能推荐、自动优化和 Prompt 编排的智能体，并用一个更完整的多语言控制台承载它。",
            heroPrimary: "进入工作室",
            heroSecondary: "查看洞察看板",
            heroVisualTitle: "优化信号",
            heroVisualTrend: "效率提升 +18%",
            overviewOneTitle: "搜索词挖掘",
            overviewOneDesc: "识别高价值搜索词，过滤浪费流量，把可复用洞察反馈到推荐链路里。",
            overviewTwoTitle: "自动优化",
            overviewTwoDesc: "把诊断结果转成预算调整、出价微调、否定词建议和带护栏的自动动作。",
            overviewThreeTitle: "Prompt 工作流",
            overviewThreeDesc: "把结构化 Prompt 设计成稳定可复用的广告分析工作流，便于团队协作。",
            chatPlaceholder: "输入命令，回车发送，Shift + Enter 换行。",
            sendMessageAria: "发送消息",
            languageSelectorAria: "语言选择器",
            quickPrompts: "快捷指令：",
            entityBannerEyebrow: "运营数据层",
            entityBannerTitle: "管理参与广告决策的人和角色。",
            entityBannerMetricOne: "活跃运营成员",
            entityBannerMetricTwo: "流程覆盖率",
            userSearchPlaceholder: "搜索框预留给后续筛选能力",
            filterAllStatuses: "全部状态",
            addUser: "新增用户",
            tableUserId: "用户 ID",
            tableUsername: "用户名",
            tableEmail: "邮箱",
            tablePhone: "电话",
            tableStatus: "状态",
            tableCreated: "创建时间",
            tableActions: "操作",
            loadingUsers: "正在加载用户...",
            previous: "上一页",
            page: "第",
            next: "下一页",
            insightEyebrow: "洞察看板",
            insightTitle: "更直观地查看账户健康度与工作流成熟度。",
            insightSparklineLabel: "工作流置信度趋势",
            totalUsers: "用户总数",
            activeUsers: "活跃用户",
            inactiveUsers: "非活跃用户",
            deletedUsers: "已删除用户",
            statusDistribution: "状态分布",
            statusDistributionNote: "与后端统计接口实时同步",
            agentCoverageTitle: "智能体覆盖度",
            agentCoverageNote: "用于规划的可视化层",
            donutCenterLabel: "已映射",
            legendOne: "分析",
            legendTwo: "优化",
            legendThree: "工作流",
            llmEyebrow: "模型运营",
            llmHeader: "LLM 配置",
            llmDesc: "配置广告分析智能体可选使用的模型服务商与调用参数。",
            providerCardTitle: "服务商",
            enableLlm: "启用 LLM 集成",
            providerLabel: "提供方",
            providerDefault: "默认模拟客户端",
            providerCustom: "自定义 API",
            providerBadgeDefault: "默认",
            apiSettingsTitle: "API 设置",
            apiKeyLabel: "API Key *",
            apiKeyPlaceholder: "请输入 API Key",
            apiKeyHint: "在这里粘贴你的服务商密钥。",
            apiEndpointLabel: "API 地址",
            apiEndpointHint: "如服务商支持，可留空并使用默认地址。",
            modelNameLabel: "模型名称",
            modelHint: "填写服务商对应的模型标识符。",
            timeoutLabel: "超时时间（秒）",
            retryLabel: "最大重试次数",
            defaultNotesTitle: "默认客户端说明",
            defaultNotesLead: "<strong>默认模拟客户端</strong> 适合本地演示和界面联调。",
            defaultNoteOne: "无需 API Key",
            defaultNoteTwo: "适合本地实验",
            defaultNoteThree: "当前项目仍然支持后续接入真实服务商",
            testConnection: "测试连接",
            saveConfig: "保存配置",
            configStatusLabel: "状态：",
            configProviderLabel: "服务商：",
            agentLabEyebrow: "智能体设计系统",
            agentLabHeader: "智能体工作室",
            agentLabDesc: "把广告分析 Agent、工作流评审链路和 Prompt 工程界面放在一个页面里进行原型设计。",
            studioMetricOneLabel: "分析深度",
            studioMetricOneValue: "5 层",
            studioMetricTwoLabel: "优化范围",
            studioMetricTwoValue: "出价 / 预算 / 搜索词",
            studioMetricThreeLabel: "Prompt 模式",
            studioMetricThreeValue: "结构化",
            runObjectiveTitle: "运行目标",
            objectiveLabel: "目标",
            objectiveDefault: "在保证盈利增长的同时提升广告活动效率。",
            runAgent: "运行智能体",
            promptTemplateTitle: "Prompt 模板",
            systemRoleLabel: "系统角色",
            taskTemplateLabel: "任务模板",
            outputStyleLabel: "输出风格",
            reloadTemplate: "重新加载模板",
            saveTemplate: "保存模板",
            agentOutputTitle: "智能体运行结果",
            workflowSteps: "工作流步骤",
            agentStepsEmpty: "运行智能体后可查看流程步骤。",
            findings: "发现问题",
            findingsEmpty: "暂时还没有发现。",
            recommendations: "优化建议",
            recommendationsEmpty: "暂时还没有建议。",
            promptPreview: "Prompt 预览",
            promptEmpty: "还没有渲染 Prompt。",
            llmOutput: "模型输出",
            llmEmpty: "还没有模型输出。",
            nextActions: "下一步动作",
            nextActionsEmpty: "还没有后续动作。",
            modalAddUser: "新增用户",
            modalEditUser: "编辑用户",
            fieldUsername: "用户名 *",
            fieldUsernamePlaceholder: "请输入用户名",
            fieldEmail: "邮箱 *",
            fieldEmailPlaceholder: "请输入邮箱",
            fieldPhone: "电话",
            fieldPhonePlaceholder: "请输入电话号码",
            fieldStatus: "状态",
            fieldTags: "标签（用逗号分隔）",
            fieldTagsPlaceholder: "运营, 核心, 试用",
            cancel: "取消",
            save: "保存",
            pageChat: "指挥中心",
            pageUsers: "实体管理",
            pageStats: "洞察看板",
            pageLlm: "模型配置",
            pageAgentLab: "智能体工作室",
            statusActive: "活跃",
            statusInactive: "非活跃",
            statusDeleted: "已删除",
            toastLoadUsersFailed: "加载用户列表失败",
            toastLoadUserDetailsFailed: "加载用户详情失败",
            toastDeleteConfirm: "确认删除该用户吗？",
            toastUserDeleted: "用户已删除",
            toastDeleteFailed: "删除失败",
            toastUserUpdated: "用户已更新",
            toastUserCreated: "用户已创建",
            toastOperationFailed: "操作失败",
            toastLoadStatisticsFailed: "加载统计数据失败",
            toastViewRefreshed: "页面已刷新",
            toastLoadConfigFailed: "加载配置失败",
            toastApiKeyRequired: "必须填写 API Key",
            toastConfigSaved: "配置已保存",
            toastSaveFailed: "保存失败",
            toastTestingConnection: "正在测试连接...",
            toastConnectionSucceeded: "连接成功",
            toastConnectionFailed: "连接失败",
            toastConnectionTestFailed: "连接测试失败",
            toastLoadPromptFailed: "加载 Prompt 模板失败",
            toastSavePromptFailed: "保存 Prompt 模板失败",
            toastPromptSaved: "Prompt 模板已保存",
            toastObjectiveRequired: "请先填写目标",
            toastRunningAgent: "正在运行智能体工作流...",
            toastAgentRunFailed: "智能体运行失败",
            toastAgentCompleted: "智能体工作流已完成",
            chatRequestFailed: "请求失败，请检查服务连接。",
            serviceOnline: "服务在线",
            serviceOffline: "连接失败",
            serviceChecking: "检测中...",
            welcomeTitle: "欢迎来到 Amazon Ads 智能体工作台。",
            welcomeLineOne: "<strong>search term mining</strong> 用于查看搜索词机会",
            welcomeLineTwo: "<strong>query all users</strong> 用于查看当前实体数据集",
            welcomeLineThree: "<strong>stats</strong> 用于检查健康指标和分布",
            welcomeLineFour: "<strong>help</strong> 用于查看支持的聊天命令",
            welcomeFooter: "左侧面板可在实体管理、指标看板、模型配置以及 Prompt 驱动的智能体工作流之间切换。",
            clearedChat: "对话已清空，输入新命令即可继续。",
            noUsersFound: "没有找到用户",
            defaultProviderName: "默认模拟客户端",
            statusEnabled: "已启用",
            statusDisabled: "未启用",
            actionEdit: "编辑",
            actionDelete: "删除",
            workflowStatusDone: "已完成",
            workflowStatusRunning: "进行中",
            workflowStatusPending: "待处理",
            openaiModelPlaceholder: "gpt-4.1 或 gpt-4o-mini",
            openaiApiHint: "请输入 OpenAI API Key",
            panguEndpointPlaceholder: "盘古服务地址",
            panguModelPlaceholder: "盘古模型名称",
            panguApiHint: "请输入盘古 API Key",
            customEndpointPlaceholder: "自定义 API 基础地址",
            customModelPlaceholder: "模型标识符",
            customApiHint: "请输入你的 API Key"
        };

        const packs = {
            es: {
                brandEyebrow: "Amazon Ads AI",
                brandTitle: "Consola del Agente",
                workspaceTitle: "Espacio de trabajo",
                settingsTitle: "Configuración",
                navChat: "Centro de mando",
                navChatHint: "Resumen y chat guiado",
                navUsers: "Entidades",
                navUsersHint: "Usuarios y operadores",
                navStats: "Panel de datos",
                navStatsHint: "Métricas y gráficos",
                navAgentLab: "Estudio del Agente",
                navAgentLabHint: "Flujo y diseño de prompts",
                navLlm: "Configuración LLM",
                navLlmHint: "Proveedor y modelo",
                serviceStatusLabel: "Estado del servicio",
                statusPill: "Automatización lista",
                topEyebrow: "Panel inteligente de operaciones",
                clearChat: "Limpiar chat",
                refresh: "Actualizar",
                heroTag: "Sistema de agente Amazon Ads",
                heroTitle: "De la minería de búsquedas a la optimización de campañas en un solo espacio.",
                heroDesc: "Crea un agente para analizar anuncios, recomendar acciones, optimizar pujas y orquestar flujos guiados por prompts.",
                heroPrimary: "Abrir estudio",
                heroSecondary: "Ver panel",
                heroVisualTitle: "Señal de optimización",
                heroVisualTrend: "+18% de eficiencia",
                overviewOneTitle: "Minería de búsquedas",
                overviewOneDesc: "Captura términos valiosos, detecta desperdicio y reutiliza insights en el ciclo de recomendación.",
                overviewTwoTitle: "Optimización automática",
                overviewTwoDesc: "Convierte diagnósticos en ajustes de presupuesto, puja y palabras negativas con reglas de seguridad.",
                overviewThreeTitle: "Flujo de prompts",
                overviewThreeDesc: "Diseña prompts estructurados y encadénalos en flujos repetibles de análisis publicitario.",
                chatPlaceholder: "Escribe un comando. Enter para enviar, Shift + Enter para nueva línea.",
                sendMessageAria: "Enviar mensaje",
                languageSelectorAria: "Selector de idioma",
                quickPrompts: "Prompts rápidos:",
                entityBannerEyebrow: "Capa operativa",
                entityBannerTitle: "Gestiona a las personas detrás de las decisiones de campaña.",
                entityBannerMetricOne: "Operadores activos",
                entityBannerMetricTwo: "Cobertura del flujo",
                userSearchPlaceholder: "Caja de búsqueda reservada para filtros futuros",
                filterAllStatuses: "Todos los estados",
                addUser: "Agregar usuario",
                tableUserId: "ID de usuario",
                tableUsername: "Nombre",
                tableEmail: "Correo",
                tablePhone: "Teléfono",
                tableStatus: "Estado",
                tableCreated: "Creado",
                tableActions: "Acciones",
                loadingUsers: "Cargando usuarios...",
                previous: "Anterior",
                page: "Página",
                next: "Siguiente",
                insightEyebrow: "Panel de insights",
                insightTitle: "Una visión más clara de la salud de la cuenta y la madurez del flujo.",
                insightSparklineLabel: "Tendencia de confianza del flujo",
                totalUsers: "Usuarios totales",
                activeUsers: "Usuarios activos",
                inactiveUsers: "Usuarios inactivos",
                deletedUsers: "Usuarios eliminados",
                statusDistribution: "Distribución de estado",
                statusDistributionNote: "Sincronizado con estadísticas del backend",
                agentCoverageTitle: "Cobertura del agente",
                agentCoverageNote: "Capa visual de planificación",
                donutCenterLabel: "Mapeado",
                legendOne: "Análisis",
                legendTwo: "Optimización",
                legendThree: "Flujo",
                llmEyebrow: "Operación del modelo",
                llmHeader: "Configuración LLM",
                llmDesc: "Configura el proveedor de modelo opcional usado por las funciones de análisis del agente.",
                providerCardTitle: "Proveedor",
                enableLlm: "Activar integración LLM",
                providerLabel: "Proveedor",
                providerDefault: "Cliente simulado por defecto",
                providerCustom: "API personalizada",
                providerBadgeDefault: "Por defecto",
                apiSettingsTitle: "Ajustes de API",
                apiKeyLabel: "API Key *",
                apiKeyPlaceholder: "Introduce la API Key",
                apiKeyHint: "Pega aquí la clave del proveedor.",
                apiEndpointLabel: "Endpoint API",
                apiEndpointHint: "Déjalo vacío para usar el valor por defecto si está disponible.",
                modelNameLabel: "Nombre del modelo",
                modelHint: "Indica el identificador del modelo usado por tu proveedor.",
                timeoutLabel: "Tiempo de espera (segundos)",
                retryLabel: "Máximo de reintentos",
                defaultNotesTitle: "Notas del cliente por defecto",
                defaultNotesLead: "<strong>El cliente simulado por defecto</strong> es útil para demos locales y pruebas de UI.",
                defaultNoteOne: "No requiere API Key",
                defaultNoteTwo: "Seguro para pruebas locales",
                defaultNoteThree: "Los proveedores reales siguen siendo opcionales",
                testConnection: "Probar conexión",
                saveConfig: "Guardar configuración",
                configStatusLabel: "Estado:",
                configProviderLabel: "Proveedor:",
                agentLabEyebrow: "Sistema de diseño del agente",
                agentLabHeader: "Estudio del Agente",
                agentLabDesc: "Prototipa el agente de análisis, el flujo de revisión y la superficie de ingeniería de prompts en un solo lugar.",
                studioMetricOneLabel: "Profundidad de análisis",
                studioMetricOneValue: "5 capas",
                studioMetricTwoLabel: "Alcance de optimización",
                studioMetricTwoValue: "Puja / Presupuesto / Consulta",
                studioMetricThreeLabel: "Modo prompt",
                studioMetricThreeValue: "Estructurado",
                runObjectiveTitle: "Objetivo de ejecución",
                objectiveLabel: "Objetivo",
                objectiveDefault: "Mejorar la eficiencia de la campaña mientras se protege el crecimiento rentable.",
                runAgent: "Ejecutar agente",
                promptTemplateTitle: "Plantilla de prompt",
                systemRoleLabel: "Rol del sistema",
                taskTemplateLabel: "Plantilla de tarea",
                outputStyleLabel: "Estilo de salida",
                reloadTemplate: "Recargar plantilla",
                saveTemplate: "Guardar plantilla",
                agentOutputTitle: "Salida del agente",
                workflowSteps: "Pasos del flujo",
                agentStepsEmpty: "Ejecuta el agente para revisar los pasos del flujo.",
                findings: "Hallazgos",
                findingsEmpty: "Aún no hay hallazgos.",
                recommendations: "Recomendaciones",
                recommendationsEmpty: "Aún no hay recomendaciones.",
                promptPreview: "Vista previa del prompt",
                promptEmpty: "Aún no hay prompt renderizado.",
                llmOutput: "Salida del LLM",
                llmEmpty: "Aún no hay salida del modelo.",
                nextActions: "Próximas acciones",
                nextActionsEmpty: "Aún no hay próximas acciones.",
                modalAddUser: "Agregar usuario",
                modalEditUser: "Editar usuario",
                fieldUsername: "Nombre de usuario *",
                fieldUsernamePlaceholder: "Introduce el nombre",
                fieldEmail: "Correo *",
                fieldEmailPlaceholder: "Introduce el correo",
                fieldPhone: "Teléfono",
                fieldPhonePlaceholder: "Introduce el teléfono",
                fieldStatus: "Estado",
                fieldTags: "Etiquetas (separadas por coma)",
                fieldTagsPlaceholder: "ops, vip, trial",
                cancel: "Cancelar",
                save: "Guardar",
                pageChat: "Centro de mando",
                pageUsers: "Entidades",
                pageStats: "Panel de datos",
                pageLlm: "Configuración LLM",
                pageAgentLab: "Estudio del Agente",
                statusActive: "Activo",
                statusInactive: "Inactivo",
                statusDeleted: "Eliminado",
                toastLoadUsersFailed: "No se pudo cargar la lista de usuarios",
                toastLoadUserDetailsFailed: "No se pudieron cargar los detalles del usuario",
                toastDeleteConfirm: "¿Eliminar este usuario?",
                toastUserDeleted: "Usuario eliminado",
                toastDeleteFailed: "No se pudo eliminar",
                toastUserUpdated: "Usuario actualizado",
                toastUserCreated: "Usuario creado",
                toastOperationFailed: "La operación falló",
                toastLoadStatisticsFailed: "No se pudieron cargar las estadísticas",
                toastViewRefreshed: "Vista actualizada",
                toastLoadConfigFailed: "No se pudo cargar la configuración",
                toastApiKeyRequired: "La API Key es obligatoria",
                toastConfigSaved: "Configuración guardada",
                toastSaveFailed: "No se pudo guardar",
                toastTestingConnection: "Probando conexión...",
                toastConnectionSucceeded: "Conexión correcta",
                toastConnectionFailed: "Conexión fallida",
                toastConnectionTestFailed: "La prueba de conexión falló",
                toastLoadPromptFailed: "No se pudo cargar la plantilla",
                toastSavePromptFailed: "No se pudo guardar la plantilla",
                toastPromptSaved: "Plantilla guardada",
                toastObjectiveRequired: "El objetivo es obligatorio",
                toastRunningAgent: "Ejecutando flujo del agente...",
                toastAgentRunFailed: "La ejecución del agente falló",
                toastAgentCompleted: "Flujo del agente completado",
                chatRequestFailed: "La solicitud falló. Revisa la conexión del servidor.",
                serviceOnline: "Servicio en línea",
                serviceOffline: "Conexión fallida",
                serviceChecking: "Comprobando...",
                welcomeTitle: "Bienvenido al espacio de trabajo del agente Amazon Ads.",
                welcomeLineOne: "<strong>search term mining</strong> para revisar oportunidades de palabras clave",
                welcomeLineTwo: "<strong>query all users</strong> para ver el conjunto actual de entidades",
                welcomeLineThree: "<strong>stats</strong> para revisar métricas y distribución",
                welcomeLineFour: "<strong>help</strong> para ver los comandos disponibles",
                welcomeFooter: "Usa los paneles de la izquierda para moverte entre gestión, métricas, configuración del modelo y flujos del agente.",
                clearedChat: "Chat limpiado. Introduce un nuevo comando para continuar.",
                noUsersFound: "No se encontraron usuarios",
                defaultProviderName: "Cliente simulado por defecto",
                statusEnabled: "Activado",
                statusDisabled: "Desactivado",
                actionEdit: "Editar",
                actionDelete: "Eliminar",
                workflowStatusDone: "Completado",
                workflowStatusRunning: "En curso",
                workflowStatusPending: "Pendiente",
                openaiModelPlaceholder: "gpt-4.1 o gpt-4o-mini",
                openaiApiHint: "Introduce una API Key de OpenAI",
                panguEndpointPlaceholder: "URL del endpoint Pangu",
                panguModelPlaceholder: "Nombre del modelo Pangu",
                panguApiHint: "Introduce una API Key de Pangu",
                customEndpointPlaceholder: "URL base de la API personalizada",
                customModelPlaceholder: "Identificador del modelo",
                customApiHint: "Introduce tu API Key"
            }
        };

        packs.fr = {
            ...packs.es,
            brandTitle: "Console de l'Agent",
            workspaceTitle: "Espace de travail",
            settingsTitle: "Paramètres",
            navChat: "Centre de commande",
            navUsers: "Entités",
            navStats: "Tableau d'analyse",
            navAgentLab: "Studio Agent",
            navLlm: "Configuration LLM",
            clearChat: "Vider le chat",
            refresh: "Actualiser",
            heroTag: "Système Agent Amazon Ads",
            heroTitle: "De la recherche de termes à l'optimisation des campagnes dans un seul espace.",
            heroDesc: "Créez un agent pour analyser les annonces, recommander des actions, optimiser les enchères et orchestrer des workflows pilotés par prompts.",
            heroPrimary: "Ouvrir le studio",
            heroSecondary: "Voir le tableau",
            heroVisualTitle: "Signal d'optimisation",
            heroVisualTrend: "+18% d'efficacité",
            chatPlaceholder: "Saisissez une commande. Entrée pour envoyer, Shift + Entrée pour une nouvelle ligne.",
            languageSelectorAria: "Sélecteur de langue",
            entityBannerTitle: "Gérez les personnes derrière les décisions de campagne.",
            addUser: "Ajouter un utilisateur",
            tableUsername: "Nom d'utilisateur",
            tablePhone: "Téléphone",
            previous: "Précédent",
            next: "Suivant",
            totalUsers: "Utilisateurs totaux",
            activeUsers: "Utilisateurs actifs",
            inactiveUsers: "Utilisateurs inactifs",
            deletedUsers: "Utilisateurs supprimés",
            providerDefault: "Client simulé par défaut",
            providerBadgeDefault: "Défaut",
            testConnection: "Tester la connexion",
            saveConfig: "Enregistrer la configuration",
            agentLabHeader: "Studio Agent",
            studioMetricOneValue: "5 niveaux",
            studioMetricThreeValue: "Structuré",
            objectiveDefault: "Améliorer l'efficacité de la campagne tout en protégeant une croissance rentable.",
            saveTemplate: "Enregistrer le modèle",
            reloadTemplate: "Recharger le modèle",
            findings: "Constats",
            recommendations: "Recommandations",
            nextActions: "Actions suivantes",
            cancel: "Annuler",
            save: "Enregistrer",
            statusActive: "Actif",
            statusInactive: "Inactif",
            statusDeleted: "Supprimé",
            actionEdit: "Modifier",
            actionDelete: "Supprimer",
            statusEnabled: "Activé",
            statusDisabled: "Désactivé",
            serviceOnline: "Service en ligne",
            serviceChecking: "Vérification..."
        };

        packs.de = {
            ...packs.es,
            brandTitle: "Agenten-Konsole",
            workspaceTitle: "Arbeitsbereich",
            settingsTitle: "Einstellungen",
            navChat: "Leitstand",
            navStats: "Insights",
            navAgentLab: "Agent Studio",
            navLlm: "LLM-Setup",
            clearChat: "Chat leeren",
            refresh: "Aktualisieren",
            heroTitle: "Von Suchbegriffen bis Kampagnenoptimierung in einem Workspace.",
            heroDesc: "Erstellen Sie einen Agenten für Anzeigenanalyse, Empfehlungen, Gebotsoptimierung und promptgesteuerte Workflows.",
            heroPrimary: "Studio öffnen",
            heroSecondary: "Dashboard anzeigen",
            heroVisualTitle: "Optimierungssignal",
            heroVisualTrend: "+18% Effizienz",
            quickPrompts: "Schnellbefehle:",
            addUser: "Benutzer hinzufügen",
            previous: "Zurück",
            next: "Weiter",
            providerDefault: "Standard-Mock-Client",
            providerBadgeDefault: "Standard",
            testConnection: "Verbindung testen",
            saveConfig: "Konfiguration speichern",
            studioMetricOneLabel: "Analysetiefe",
            studioMetricOneValue: "5 Ebenen",
            studioMetricTwoLabel: "Optimierungsumfang",
            studioMetricTwoValue: "Gebot / Budget / Suche",
            studioMetricThreeLabel: "Prompt-Modus",
            objectiveDefault: "Kampagneneffizienz verbessern und gleichzeitig profitables Wachstum schützen.",
            cancel: "Abbrechen",
            save: "Speichern",
            statusActive: "Aktiv",
            statusInactive: "Inaktiv",
            statusDeleted: "Gelöscht",
            actionEdit: "Bearbeiten",
            actionDelete: "Löschen",
            statusEnabled: "Aktiviert",
            statusDisabled: "Deaktiviert",
            serviceOnline: "Dienst online",
            serviceChecking: "Wird geprüft..."
        };

        packs.pt = {
            ...packs.es,
            brandTitle: "Console do Agente",
            workspaceTitle: "Espaço de trabalho",
            settingsTitle: "Configurações",
            navChat: "Central de comando",
            navStats: "Painel de insights",
            navAgentLab: "Estúdio do Agente",
            navLlm: "Configuração LLM",
            clearChat: "Limpar chat",
            refresh: "Atualizar",
            heroTitle: "Da mineração de termos de busca à otimização de campanhas em um só espaço.",
            heroDesc: "Crie um agente para analisar anúncios, recomendar ações, otimizar lances e orquestrar fluxos guiados por prompts.",
            heroPrimary: "Abrir estúdio",
            heroSecondary: "Ver painel",
            heroVisualTitle: "Sinal de otimização",
            heroVisualTrend: "+18% de eficiência",
            addUser: "Adicionar usuário",
            previous: "Anterior",
            next: "Próxima",
            providerDefault: "Cliente simulado padrão",
            providerBadgeDefault: "Padrão",
            testConnection: "Testar conexão",
            saveConfig: "Salvar configuração",
            objectiveDefault: "Melhorar a eficiência da campanha enquanto protege o crescimento lucrativo.",
            cancel: "Cancelar",
            save: "Salvar",
            statusActive: "Ativo",
            statusInactive: "Inativo",
            statusDeleted: "Excluído",
            actionEdit: "Editar",
            actionDelete: "Excluir",
            statusEnabled: "Ativado",
            statusDisabled: "Desativado",
            serviceOnline: "Serviço online",
            serviceChecking: "Verificando..."
        };

        packs.ja = {
            ...packs.es,
            brandTitle: "エージェントコンソール",
            workspaceTitle: "ワークスペース",
            settingsTitle: "設定",
            navChat: "コマンドセンター",
            navUsers: "エンティティ",
            navStats: "インサイト",
            navAgentLab: "エージェントスタジオ",
            navLlm: "LLM 設定",
            clearChat: "チャットを消去",
            refresh: "更新",
            heroTag: "Amazon Ads エージェントシステム",
            heroTitle: "検索語分析からキャンペーン最適化までを一つの画面で。",
            heroDesc: "広告分析、推奨、入札最適化、プロンプト駆動ワークフローを扱うエージェントを構築できます。",
            heroPrimary: "スタジオを開く",
            heroSecondary: "ダッシュボードを見る",
            heroVisualTitle: "最適化シグナル",
            heroVisualTrend: "効率 +18%",
            overviewOneTitle: "検索語分析",
            overviewTwoTitle: "自動最適化",
            overviewThreeTitle: "Prompt ワークフロー",
            chatPlaceholder: "コマンドを入力。Enter で送信、Shift + Enter で改行。",
            sendMessageAria: "メッセージを送信",
            languageSelectorAria: "言語セレクター",
            quickPrompts: "クイックプロンプト:",
            addUser: "ユーザー追加",
            previous: "前へ",
            next: "次へ",
            page: "ページ",
            providerDefault: "デフォルトのモッククライアント",
            providerBadgeDefault: "標準",
            testConnection: "接続テスト",
            saveConfig: "設定を保存",
            studioMetricOneLabel: "分析深度",
            studioMetricOneValue: "5 レイヤー",
            studioMetricTwoLabel: "最適化範囲",
            studioMetricTwoValue: "入札 / 予算 / 検索語",
            studioMetricThreeLabel: "Prompt モード",
            studioMetricThreeValue: "構造化",
            objectiveDefault: "利益成長を守りながら、キャンペーン効率を改善する。",
            findings: "検出事項",
            recommendations: "推奨事項",
            nextActions: "次のアクション",
            cancel: "キャンセル",
            save: "保存",
            statusActive: "有効",
            statusInactive: "無効",
            statusDeleted: "削除済み",
            actionEdit: "編集",
            actionDelete: "削除",
            statusEnabled: "有効",
            statusDisabled: "無効",
            serviceOnline: "サービス稼働中",
            serviceChecking: "確認中..."
        };

        packs.ar = {
            ...packs.es,
            brandTitle: "لوحة الوكيل",
            workspaceTitle: "مساحة العمل",
            settingsTitle: "الإعدادات",
            navChat: "مركز القيادة",
            navChatHint: "نظرة عامة ومحادثة موجهة",
            navUsers: "الكيانات",
            navUsersHint: "المستخدمون والمشغلون",
            navStats: "لوحة الرؤى",
            navStatsHint: "مقاييس ورسوم بيانية",
            navAgentLab: "استوديو الوكيل",
            navAgentLabHint: "سير العمل وتصميم الموجهات",
            navLlm: "إعداد LLM",
            navLlmHint: "المزوّد والنموذج",
            serviceStatusLabel: "حالة الخدمة",
            statusPill: "الأتمتة جاهزة",
            topEyebrow: "لوحة تشغيل ذكية",
            clearChat: "مسح المحادثة",
            refresh: "تحديث",
            heroTag: "نظام وكيل Amazon Ads",
            heroTitle: "من تحليل عبارات البحث إلى تحسين الحملات في مساحة واحدة.",
            heroDesc: "أنشئ وكيلاً لتحليل الإعلانات واقتراح الإجراءات وتحسين العروض وسير العمل المعتمد على الموجهات.",
            heroPrimary: "فتح الاستوديو",
            heroSecondary: "عرض اللوحة",
            heroVisualTitle: "إشارة التحسين",
            heroVisualTrend: "+18% كفاءة",
            overviewOneTitle: "تحليل عبارات البحث",
            overviewTwoTitle: "تحسين تلقائي",
            overviewThreeTitle: "سير عمل Prompt",
            chatPlaceholder: "اكتب أمراً. Enter للإرسال و Shift + Enter لسطر جديد.",
            sendMessageAria: "إرسال الرسالة",
            languageSelectorAria: "محدد اللغة",
            quickPrompts: "أوامر سريعة:",
            entityBannerEyebrow: "طبقة التشغيل",
            entityBannerTitle: "إدارة الأشخاص وراء قرارات الحملات.",
            entityBannerMetricOne: "المشغلون النشطون",
            entityBannerMetricTwo: "تغطية سير العمل",
            userSearchPlaceholder: "حقل البحث مخصص للفلاتر القادمة",
            filterAllStatuses: "كل الحالات",
            addUser: "إضافة مستخدم",
            tableUserId: "معرّف المستخدم",
            tableUsername: "اسم المستخدم",
            tableEmail: "البريد الإلكتروني",
            tablePhone: "الهاتف",
            tableStatus: "الحالة",
            tableCreated: "تاريخ الإنشاء",
            tableActions: "الإجراءات",
            loadingUsers: "جارٍ تحميل المستخدمين...",
            previous: "السابق",
            page: "الصفحة",
            next: "التالي",
            insightEyebrow: "لوحة الرؤى",
            insightTitle: "رؤية أوضح لصحة الحساب ونضج سير العمل.",
            insightSparklineLabel: "اتجاه ثقة سير العمل",
            totalUsers: "إجمالي المستخدمين",
            activeUsers: "المستخدمون النشطون",
            inactiveUsers: "المستخدمون غير النشطين",
            deletedUsers: "المستخدمون المحذوفون",
            statusDistribution: "توزيع الحالات",
            statusDistributionNote: "متزامن مع إحصاءات الخلفية",
            agentCoverageTitle: "تغطية الوكيل",
            agentCoverageNote: "طبقة تخطيط مرئية",
            donutCenterLabel: "مربوط",
            legendOne: "تحليل",
            legendTwo: "تحسين",
            legendThree: "سير العمل",
            llmEyebrow: "تشغيل النموذج",
            llmHeader: "إعداد LLM",
            llmDesc: "اضبط مزوّد النموذج الاختياري المستخدم في ميزات تحليل الوكيل.",
            providerCardTitle: "المزوّد",
            enableLlm: "تفعيل تكامل LLM",
            providerLabel: "المزوّد",
            providerDefault: "عميل افتراضي تجريبي",
            providerCustom: "واجهة API مخصصة",
            providerBadgeDefault: "افتراضي",
            apiSettingsTitle: "إعدادات API",
            apiKeyLabel: "API Key *",
            apiKeyPlaceholder: "أدخل API Key",
            apiKeyHint: "ألصق مفتاح المزوّد هنا.",
            apiEndpointLabel: "عنوان API",
            apiEndpointHint: "اتركه فارغاً لاستخدام الإعداد الافتراضي إذا كان مدعوماً.",
            modelNameLabel: "اسم النموذج",
            modelHint: "حدّد معرّف النموذج المستخدم من مزوّدك.",
            timeoutLabel: "مهلة الانتظار (ثانية)",
            retryLabel: "أقصى عدد لإعادة المحاولة",
            defaultNotesTitle: "ملاحظات العميل الافتراضي",
            defaultNotesLead: "<strong>العميل التجريبي الافتراضي</strong> مفيد للعروض المحلية واختبار الواجهة.",
            defaultNoteOne: "لا يحتاج إلى API Key",
            defaultNoteTwo: "آمن للتجارب المحلية",
            defaultNoteThree: "المزوّدون الحقيقيون ما زالوا اختياريين",
            testConnection: "اختبار الاتصال",
            saveConfig: "حفظ الإعداد",
            configStatusLabel: "الحالة:",
            configProviderLabel: "المزوّد:",
            agentLabEyebrow: "نظام تصميم الوكيل",
            agentLabHeader: "استوديو الوكيل",
            agentLabDesc: "صمّم نموذج وكيل التحليل وسير عمل المراجعة وهندسة الموجهات في مكان واحد.",
            studioMetricOneLabel: "عمق التحليل",
            studioMetricOneValue: "5 طبقات",
            studioMetricTwoLabel: "نطاق التحسين",
            studioMetricTwoValue: "العرض / الميزانية / الاستعلام",
            studioMetricThreeLabel: "وضع Prompt",
            studioMetricThreeValue: "منظم",
            runObjectiveTitle: "هدف التشغيل",
            objectiveLabel: "الهدف",
            objectiveDefault: "تحسين كفاءة الحملة مع الحفاظ على النمو المربح.",
            runAgent: "تشغيل الوكيل",
            promptTemplateTitle: "قالب Prompt",
            systemRoleLabel: "دور النظام",
            taskTemplateLabel: "قالب المهمة",
            outputStyleLabel: "أسلوب الإخراج",
            reloadTemplate: "إعادة تحميل القالب",
            saveTemplate: "حفظ القالب",
            agentOutputTitle: "نتائج تشغيل الوكيل",
            workflowSteps: "خطوات سير العمل",
            agentStepsEmpty: "شغّل الوكيل لمراجعة خطوات سير العمل.",
            findings: "النتائج",
            findingsEmpty: "لا توجد نتائج بعد.",
            recommendations: "التوصيات",
            recommendationsEmpty: "لا توجد توصيات بعد.",
            promptPreview: "معاينة Prompt",
            promptEmpty: "لم يتم إنشاء Prompt بعد.",
            llmOutput: "مخرجات LLM",
            llmEmpty: "لا توجد مخرجات للنموذج بعد.",
            nextActions: "الإجراءات التالية",
            nextActionsEmpty: "لا توجد إجراءات تالية بعد.",
            modalAddUser: "إضافة مستخدم",
            modalEditUser: "تعديل المستخدم",
            fieldUsername: "اسم المستخدم *",
            fieldUsernamePlaceholder: "أدخل اسم المستخدم",
            fieldEmail: "البريد الإلكتروني *",
            fieldEmailPlaceholder: "أدخل البريد الإلكتروني",
            fieldPhone: "الهاتف",
            fieldPhonePlaceholder: "أدخل رقم الهاتف",
            fieldStatus: "الحالة",
            fieldTags: "الوسوم (مفصولة بفاصلة)",
            fieldTagsPlaceholder: "ops, vip, trial",
            cancel: "إلغاء",
            save: "حفظ",
            pageChat: "مركز القيادة",
            pageUsers: "الكيانات",
            pageStats: "لوحة الرؤى",
            pageLlm: "إعداد LLM",
            pageAgentLab: "استوديو الوكيل",
            statusActive: "نشط",
            statusInactive: "غير نشط",
            statusDeleted: "محذوف",
            toastLoadUsersFailed: "تعذر تحميل قائمة المستخدمين",
            toastLoadUserDetailsFailed: "تعذر تحميل تفاصيل المستخدم",
            toastDeleteConfirm: "هل تريد حذف هذا المستخدم؟",
            toastUserDeleted: "تم حذف المستخدم",
            toastDeleteFailed: "فشل الحذف",
            toastUserUpdated: "تم تحديث المستخدم",
            toastUserCreated: "تم إنشاء المستخدم",
            toastOperationFailed: "فشلت العملية",
            toastLoadStatisticsFailed: "تعذر تحميل الإحصاءات",
            toastViewRefreshed: "تم تحديث الصفحة",
            toastLoadConfigFailed: "تعذر تحميل الإعداد",
            toastApiKeyRequired: "API Key مطلوب",
            toastConfigSaved: "تم حفظ الإعداد",
            toastSaveFailed: "فشل الحفظ",
            toastTestingConnection: "جارٍ اختبار الاتصال...",
            toastConnectionSucceeded: "تم الاتصال بنجاح",
            toastConnectionFailed: "فشل الاتصال",
            toastConnectionTestFailed: "فشل اختبار الاتصال",
            toastLoadPromptFailed: "تعذر تحميل القالب",
            toastSavePromptFailed: "تعذر حفظ القالب",
            toastPromptSaved: "تم حفظ القالب",
            toastObjectiveRequired: "الهدف مطلوب",
            toastRunningAgent: "جارٍ تشغيل سير عمل الوكيل...",
            toastAgentRunFailed: "فشل تشغيل الوكيل",
            toastAgentCompleted: "اكتمل سير عمل الوكيل",
            chatRequestFailed: "فشل الطلب. يرجى التحقق من اتصال الخادم.",
            serviceOnline: "الخدمة متصلة",
            serviceOffline: "فشل الاتصال",
            serviceChecking: "جارٍ التحقق...",
            welcomeTitle: "مرحباً بك في مساحة عمل وكيل Amazon Ads.",
            welcomeLineOne: "<strong>search term mining</strong> لفحص فرص الكلمات المفتاحية",
            welcomeLineTwo: "<strong>query all users</strong> لعرض مجموعة الكيانات الحالية",
            welcomeLineThree: "<strong>stats</strong> لمراجعة المقاييس والتوزيع",
            welcomeLineFour: "<strong>help</strong> لمراجعة الأوامر المتاحة",
            welcomeFooter: "استخدم اللوحات الجانبية للتنقل بين الإدارة والمقاييس وإعداد النموذج وسير عمل الوكيل.",
            clearedChat: "تم مسح المحادثة. أدخل أمراً جديداً للمتابعة.",
            noUsersFound: "لم يتم العثور على مستخدمين",
            defaultProviderName: "عميل تجريبي افتراضي",
            statusEnabled: "مفعّل",
            statusDisabled: "غير مفعّل",
            actionEdit: "تعديل",
            actionDelete: "حذف",
            workflowStatusDone: "مكتمل",
            workflowStatusRunning: "قيد التنفيذ",
            workflowStatusPending: "قيد الانتظار",
            openaiModelPlaceholder: "gpt-4.1 أو gpt-4o-mini",
            openaiApiHint: "أدخل API Key لـ OpenAI",
            panguEndpointPlaceholder: "رابط خدمة Pangu",
            panguModelPlaceholder: "اسم نموذج Pangu",
            panguApiHint: "أدخل API Key لـ Pangu",
            customEndpointPlaceholder: "رابط API المخصص",
            customModelPlaceholder: "معرّف النموذج",
            customApiHint: "أدخل API Key الخاص بك"
        };

        Object.assign(packs, {
            es: {
                ...packs.es,
                metricCtr: "CTR",
                metricAcos: "ACOS",
                metricRoas: "ROAS",
                openaiEndpointPlaceholder: "https://api.openai.com/v1"
            },
            fr: {
                ...en,
                brandTitle: "Console de l'agent",
                workspaceTitle: "Espace de travail",
                settingsTitle: "Paramètres",
                navChat: "Centre de commande",
                navChatHint: "Vue d'ensemble et chat guidé",
                navUsers: "Entités",
                navUsersHint: "Utilisateurs et opérateurs",
                navStats: "Insights",
                navStatsHint: "Métriques et graphiques en direct",
                navAgentLab: "Studio Agent",
                navAgentLabHint: "Workflow et conception de prompts",
                navLlm: "Configuration LLM",
                navLlmHint: "Fournisseur et paramètres du modèle",
                serviceStatusLabel: "État du service",
                statusPill: "Automatisation prête",
                topEyebrow: "Tableau de bord des opérations intelligentes",
                clearChat: "Vider le chat",
                refresh: "Actualiser",
                heroTag: "Système Agent Amazon Ads",
                heroTitle: "De l'analyse des termes de recherche à l'optimisation des campagnes dans un seul espace.",
                heroDesc: "Créez un agent pour analyser les annonces, recommander des actions, optimiser les enchères et orchestrer des workflows pilotés par prompts.",
                heroPrimary: "Ouvrir le studio",
                heroSecondary: "Voir le tableau",
                heroVisualTitle: "Signal d'optimisation",
                heroVisualTrend: "+18% d'efficacité",
                metricCtr: "CTR",
                metricAcos: "ACOS",
                metricRoas: "ROAS",
                overviewOneTitle: "Analyse des recherches",
                overviewOneDesc: "Capturez les termes à forte valeur, isolez le gaspillage et réinjectez les insights dans la boucle de recommandation.",
                overviewTwoTitle: "Optimisation automatique",
                overviewTwoDesc: "Transformez les diagnostics en ajustements de budget, de bid et de mots-clés négatifs avec garde-fous.",
                overviewThreeTitle: "Workflow Prompt",
                overviewThreeDesc: "Concevez des prompts structurés et assemblez-les en workflows publicitaires réutilisables.",
                chatPlaceholder: "Saisissez une commande. Entrée pour envoyer, Shift + Entrée pour une nouvelle ligne.",
                sendMessageAria: "Envoyer le message",
                languageSelectorAria: "Sélecteur de langue",
                quickPrompts: "Prompts rapides :",
                entityBannerEyebrow: "Couche opérationnelle",
                entityBannerTitle: "Gérez les personnes derrière les décisions de campagne.",
                entityBannerMetricOne: "Opérateurs actifs",
                entityBannerMetricTwo: "Couverture du workflow",
                userSearchPlaceholder: "Champ de recherche réservé aux futurs filtres",
                filterAllStatuses: "Tous les statuts",
                addUser: "Ajouter un utilisateur",
                tableUserId: "ID utilisateur",
                tableUsername: "Nom d'utilisateur",
                tableEmail: "E-mail",
                tablePhone: "Téléphone",
                tableStatus: "Statut",
                tableCreated: "Créé le",
                tableActions: "Actions",
                loadingUsers: "Chargement des utilisateurs...",
                previous: "Précédent",
                page: "Page",
                next: "Suivant",
                insightEyebrow: "Tableau d'insights",
                insightTitle: "Une vue plus claire de la santé du compte et de la maturité du workflow.",
                insightSparklineLabel: "Tendance de confiance du workflow",
                totalUsers: "Utilisateurs totaux",
                activeUsers: "Utilisateurs actifs",
                inactiveUsers: "Utilisateurs inactifs",
                deletedUsers: "Utilisateurs supprimés",
                statusDistribution: "Répartition des statuts",
                statusDistributionNote: "Synchronisé avec les statistiques du backend",
                agentCoverageTitle: "Couverture de l'agent",
                agentCoverageNote: "Couche visuelle de planification",
                donutCenterLabel: "Cartographié",
                legendOne: "Analyse",
                legendTwo: "Optimisation",
                legendThree: "Workflow",
                llmEyebrow: "Opérations du modèle",
                llmHeader: "Configuration LLM",
                llmDesc: "Configurez le fournisseur de modèle optionnel utilisé par les fonctions d'analyse de l'agent.",
                providerCardTitle: "Fournisseur",
                enableLlm: "Activer l'intégration LLM",
                providerLabel: "Fournisseur",
                providerDefault: "Client mock par défaut",
                providerCustom: "API personnalisée",
                providerBadgeDefault: "Défaut",
                apiSettingsTitle: "Paramètres API",
                apiKeyLabel: "Clé API *",
                apiKeyPlaceholder: "Saisissez la clé API",
                apiKeyHint: "Collez ici la clé de votre fournisseur.",
                apiEndpointLabel: "Point de terminaison API",
                apiEndpointHint: "Laissez vide pour utiliser la valeur par défaut si elle est prise en charge.",
                modelNameLabel: "Nom du modèle",
                modelHint: "Définissez l'identifiant du modèle utilisé par votre fournisseur.",
                timeoutLabel: "Délai d'attente (secondes)",
                retryLabel: "Nombre maximal de tentatives",
                defaultNotesTitle: "Notes du client par défaut",
                defaultNotesLead: "<strong>Le client mock par défaut</strong> est utile pour les démos locales et les tests UI.",
                defaultNoteOne: "Aucune clé API requise",
                defaultNoteTwo: "Sûr pour les expérimentations locales",
                defaultNoteThree: "Les fournisseurs réels restent optionnels",
                testConnection: "Tester la connexion",
                saveConfig: "Enregistrer la configuration",
                configStatusLabel: "Statut :",
                configProviderLabel: "Fournisseur :",
                agentLabEyebrow: "Système de conception d'agent",
                agentLabHeader: "Studio Agent",
                agentLabDesc: "Prototypez l'agent d'analyse, la boucle de revue du workflow et la surface d'ingénierie des prompts en un seul endroit.",
                studioMetricOneLabel: "Profondeur d'analyse",
                studioMetricOneValue: "5 niveaux",
                studioMetricTwoLabel: "Portée de l'optimisation",
                studioMetricTwoValue: "Bid / Budget / Requête",
                studioMetricThreeLabel: "Mode Prompt",
                studioMetricThreeValue: "Structuré",
                runObjectiveTitle: "Objectif d'exécution",
                objectiveLabel: "Objectif",
                objectiveDefault: "Améliorer l'efficacité de la campagne tout en protégeant une croissance rentable.",
                runAgent: "Exécuter l'agent",
                promptTemplateTitle: "Modèle de prompt",
                systemRoleLabel: "Rôle système",
                taskTemplateLabel: "Modèle de tâche",
                outputStyleLabel: "Style de sortie",
                reloadTemplate: "Recharger le modèle",
                saveTemplate: "Enregistrer le modèle",
                agentOutputTitle: "Résultat de l'agent",
                workflowSteps: "Étapes du workflow",
                agentStepsEmpty: "Exécutez l'agent pour examiner les étapes du workflow.",
                findings: "Constats",
                findingsEmpty: "Aucun constat pour le moment.",
                recommendations: "Recommandations",
                recommendationsEmpty: "Aucune recommandation pour le moment.",
                promptPreview: "Aperçu du prompt",
                promptEmpty: "Aucun prompt généré pour le moment.",
                llmOutput: "Sortie LLM",
                llmEmpty: "Aucune sortie du modèle pour le moment.",
                nextActions: "Actions suivantes",
                nextActionsEmpty: "Aucune action suivante pour le moment.",
                modalAddUser: "Ajouter un utilisateur",
                modalEditUser: "Modifier l'utilisateur",
                fieldUsername: "Nom d'utilisateur *",
                fieldUsernamePlaceholder: "Saisissez le nom d'utilisateur",
                fieldEmail: "E-mail *",
                fieldEmailPlaceholder: "Saisissez l'e-mail",
                fieldPhone: "Téléphone",
                fieldPhonePlaceholder: "Saisissez le numéro",
                fieldStatus: "Statut",
                fieldTags: "Tags (séparés par des virgules)",
                cancel: "Annuler",
                save: "Enregistrer",
                pageChat: "Centre de commande",
                pageUsers: "Entités",
                pageStats: "Insights",
                pageLlm: "Configuration LLM",
                pageAgentLab: "Studio Agent",
                statusActive: "Actif",
                statusInactive: "Inactif",
                statusDeleted: "Supprimé",
                serviceOnline: "Service en ligne",
                serviceChecking: "Vérification..."
            },
            de: {
                ...en,
                brandTitle: "Agent-Konsole",
                workspaceTitle: "Arbeitsbereich",
                settingsTitle: "Einstellungen",
                navChat: "Leitstand",
                navChatHint: "Übersicht und geführter Chat",
                navUsers: "Entitäten",
                navUsersHint: "Benutzer und Operatoren",
                navStats: "Einblicke",
                navStatsHint: "Live-Metriken und Diagramme",
                navAgentLab: "Agent Studio",
                navAgentLabHint: "Workflow- und Prompt-Design",
                navLlm: "LLM-Setup",
                navLlmHint: "Anbieter und Modellparameter",
                serviceStatusLabel: "Dienststatus",
                statusPill: "Automatisierung bereit",
                topEyebrow: "Intelligentes Operations-Dashboard",
                clearChat: "Chat leeren",
                refresh: "Aktualisieren",
                heroTitle: "Von Suchbegriffen bis zur Kampagnenoptimierung in einem Workspace.",
                heroDesc: "Erstellen Sie einen Agenten für Anzeigenanalyse, Empfehlungen, Gebotsoptimierung und promptgesteuerte Workflows.",
                heroPrimary: "Studio öffnen",
                heroSecondary: "Dashboard anzeigen",
                heroVisualTitle: "Optimierungssignal",
                heroVisualTrend: "+18% Effizienz",
                metricCtr: "CTR",
                metricAcos: "ACOS",
                metricRoas: "ROAS",
                overviewOneTitle: "Suchbegriff-Analyse",
                overviewOneDesc: "Erfassen Sie wertvolle Suchbegriffe, isolieren Sie Verschwendung und speisen Sie Insights zurück in die Empfehlungsschleife.",
                overviewTwoTitle: "Automatische Optimierung",
                overviewTwoDesc: "Wandeln Sie Diagnosen in Budgetanpassungen, Gebotsoptimierung und Negativ-Keyword-Vorschläge mit Leitplanken um.",
                overviewThreeTitle: "Prompt-Workflow",
                overviewThreeDesc: "Entwerfen Sie strukturierte Prompts und verketten Sie sie zu wiederverwendbaren Analyse-Workflows.",
                quickPrompts: "Schnellbefehle:",
                entityBannerEyebrow: "Betriebsebene",
                entityBannerTitle: "Verwalten Sie die Menschen hinter den Kampagnenentscheidungen.",
                entityBannerMetricOne: "Aktive Operatoren",
                entityBannerMetricTwo: "Workflow-Abdeckung",
                userSearchPlaceholder: "Suchfeld für künftige Filter reserviert",
                filterAllStatuses: "Alle Status",
                addUser: "Benutzer hinzufügen",
                tableUserId: "Benutzer-ID",
                tableUsername: "Benutzername",
                tableEmail: "E-Mail",
                tablePhone: "Telefon",
                tableStatus: "Status",
                tableCreated: "Erstellt",
                tableActions: "Aktionen",
                loadingUsers: "Benutzer werden geladen...",
                previous: "Zurück",
                page: "Seite",
                next: "Weiter",
                insightEyebrow: "Insights-Dashboard",
                insightTitle: "Ein klareres Bild von Kontogesundheit und Workflow-Reife.",
                insightSparklineLabel: "Workflow-Vertrauenstrend",
                totalUsers: "Benutzer gesamt",
                activeUsers: "Aktive Benutzer",
                inactiveUsers: "Inaktive Benutzer",
                deletedUsers: "Gelöschte Benutzer",
                statusDistribution: "Statusverteilung",
                statusDistributionNote: "Mit Backend-Statistiken synchronisiert",
                agentCoverageTitle: "Agent-Abdeckung",
                agentCoverageNote: "Visuelle Planungsebene",
                donutCenterLabel: "Abgebildet",
                legendOne: "Analyse",
                legendTwo: "Optimierung",
                legendThree: "Workflow",
                llmEyebrow: "Modellbetrieb",
                llmHeader: "LLM-Konfiguration",
                llmDesc: "Konfigurieren Sie den optionalen Modellanbieter, der von den Analysefunktionen des Agenten verwendet wird.",
                providerCardTitle: "Anbieter",
                enableLlm: "LLM-Integration aktivieren",
                providerLabel: "Anbieter",
                providerDefault: "Standard-Mock-Client",
                providerCustom: "Benutzerdefinierte API",
                providerBadgeDefault: "Standard",
                apiSettingsTitle: "API-Einstellungen",
                apiKeyLabel: "API-Schlüssel *",
                apiKeyPlaceholder: "API-Schlüssel eingeben",
                apiKeyHint: "Fügen Sie hier den Schlüssel Ihres Anbieters ein.",
                apiEndpointLabel: "API-Endpunkt",
                apiEndpointHint: "Leer lassen, um falls unterstützt den Standardwert zu verwenden.",
                modelNameLabel: "Modellname",
                modelHint: "Geben Sie die Modellkennung Ihres Anbieters an.",
                timeoutLabel: "Zeitlimit (Sekunden)",
                retryLabel: "Maximale Wiederholungen",
                defaultNotesTitle: "Hinweise zum Standard-Client",
                defaultNotesLead: "<strong>Der Standard-Mock-Client</strong> ist nützlich für lokale Demos und UI-Tests.",
                defaultNoteOne: "Kein API-Schlüssel erforderlich",
                defaultNoteTwo: "Sicher für lokale Experimente",
                defaultNoteThree: "Echte Anbieter bleiben optional",
                testConnection: "Verbindung testen",
                saveConfig: "Konfiguration speichern",
                configStatusLabel: "Status:",
                configProviderLabel: "Anbieter:",
                agentLabEyebrow: "Agent-Designsystem",
                agentLabHeader: "Agent Studio",
                agentLabDesc: "Prototypisieren Sie den Analyse-Agenten, die Review-Schleife und die Prompt-Engineering-Oberfläche an einem Ort.",
                studioMetricOneLabel: "Analysetiefe",
                studioMetricOneValue: "5 Ebenen",
                studioMetricTwoLabel: "Optimierungsumfang",
                studioMetricTwoValue: "Gebot / Budget / Suchanfrage",
                studioMetricThreeLabel: "Prompt-Modus",
                studioMetricThreeValue: "Strukturiert",
                runObjectiveTitle: "Ausführungsziel",
                objectiveLabel: "Ziel",
                objectiveDefault: "Kampagneneffizienz verbessern und gleichzeitig profitables Wachstum schützen.",
                runAgent: "Agent ausführen",
                promptTemplateTitle: "Prompt-Vorlage",
                systemRoleLabel: "Systemrolle",
                taskTemplateLabel: "Aufgabenvorlage",
                outputStyleLabel: "Ausgabestil",
                reloadTemplate: "Vorlage neu laden",
                saveTemplate: "Vorlage speichern",
                agentOutputTitle: "Agent-Ausgabe",
                workflowSteps: "Workflow-Schritte",
                agentStepsEmpty: "Führen Sie den Agenten aus, um die Workflow-Schritte zu prüfen.",
                findings: "Erkenntnisse",
                findingsEmpty: "Noch keine Erkenntnisse.",
                recommendations: "Empfehlungen",
                recommendationsEmpty: "Noch keine Empfehlungen.",
                promptPreview: "Prompt-Vorschau",
                promptEmpty: "Noch kein gerenderter Prompt.",
                llmOutput: "LLM-Ausgabe",
                llmEmpty: "Noch keine Modellausgabe.",
                nextActions: "Nächste Schritte",
                nextActionsEmpty: "Noch keine nächsten Schritte.",
                cancel: "Abbrechen",
                save: "Speichern",
                pageChat: "Leitstand",
                pageUsers: "Entitäten",
                pageStats: "Einblicke",
                pageLlm: "LLM-Setup",
                pageAgentLab: "Agent Studio",
                statusActive: "Aktiv",
                statusInactive: "Inaktiv",
                statusDeleted: "Gelöscht",
                serviceOnline: "Dienst online",
                serviceChecking: "Wird geprüft..."
            },
            pt: {
                ...en,
                brandTitle: "Console do Agente",
                workspaceTitle: "Espaço de trabalho",
                settingsTitle: "Configurações",
                navChat: "Central de comando",
                navChatHint: "Visão geral e chat guiado",
                navUsers: "Entidades",
                navUsersHint: "Usuários e operadores",
                navStats: "Painel de insights",
                navStatsHint: "Métricas e gráficos ao vivo",
                navAgentLab: "Estúdio do Agente",
                navAgentLabHint: "Fluxo de trabalho e design de prompts",
                navLlm: "Configuração LLM",
                navLlmHint: "Fornecedor e parâmetros do modelo",
                serviceStatusLabel: "Status do serviço",
                statusPill: "Automação pronta",
                topEyebrow: "Painel inteligente de operações",
                clearChat: "Limpar chat",
                refresh: "Atualizar",
                heroTitle: "Da mineração de termos de busca à otimização de campanhas em um só espaço.",
                heroDesc: "Crie um agente para analisar anúncios, recomendar ações, otimizar lances e orquestrar fluxos guiados por prompts.",
                heroPrimary: "Abrir estúdio",
                heroSecondary: "Ver painel",
                heroVisualTitle: "Sinal de otimização",
                heroVisualTrend: "+18% de eficiência",
                metricCtr: "CTR",
                metricAcos: "ACOS",
                metricRoas: "ROAS",
                overviewOneTitle: "Mineração de buscas",
                overviewOneDesc: "Capture termos valiosos, isole desperdícios e reutilize insights no ciclo de recomendação.",
                overviewTwoTitle: "Otimização automática",
                overviewTwoDesc: "Transforme diagnósticos em ajustes de orçamento, lances e palavras negativas com trilhos de segurança.",
                overviewThreeTitle: "Fluxo de Prompt",
                overviewThreeDesc: "Projete prompts estruturados e encadeie-os em fluxos repetíveis de análise de anúncios.",
                entityBannerEyebrow: "Camada operacional",
                entityBannerTitle: "Gerencie as pessoas por trás das decisões de campanha.",
                entityBannerMetricOne: "Operadores ativos",
                entityBannerMetricTwo: "Cobertura do fluxo",
                userSearchPlaceholder: "Campo de busca reservado para filtros futuros",
                filterAllStatuses: "Todos os status",
                addUser: "Adicionar usuário",
                tableUserId: "ID do usuário",
                tableUsername: "Nome de usuário",
                tableEmail: "E-mail",
                tablePhone: "Telefone",
                tableStatus: "Status",
                tableCreated: "Criado em",
                tableActions: "Ações",
                loadingUsers: "Carregando usuários...",
                previous: "Anterior",
                page: "Página",
                next: "Próxima",
                insightEyebrow: "Painel de insights",
                insightTitle: "Uma visão mais clara da saúde da conta e da maturidade do fluxo.",
                insightSparklineLabel: "Tendência de confiança do fluxo",
                totalUsers: "Usuários totais",
                activeUsers: "Usuários ativos",
                inactiveUsers: "Usuários inativos",
                deletedUsers: "Usuários excluídos",
                statusDistribution: "Distribuição de status",
                statusDistributionNote: "Sincronizado com estatísticas do backend",
                agentCoverageTitle: "Cobertura do agente",
                agentCoverageNote: "Camada visual de planejamento",
                donutCenterLabel: "Mapeado",
                legendOne: "Análise",
                legendTwo: "Otimização",
                legendThree: "Fluxo",
                llmEyebrow: "Operação do modelo",
                llmHeader: "Configuração LLM",
                llmDesc: "Configure o provedor de modelo opcional usado pelos recursos de análise do agente.",
                providerCardTitle: "Fornecedor",
                enableLlm: "Ativar integração LLM",
                providerLabel: "Fornecedor",
                providerDefault: "Cliente simulado padrão",
                providerCustom: "API personalizada",
                providerBadgeDefault: "Padrão",
                apiSettingsTitle: "Configurações da API",
                apiKeyLabel: "Chave da API *",
                apiKeyPlaceholder: "Digite a chave da API",
                apiKeyHint: "Cole aqui a chave do provedor.",
                apiEndpointLabel: "Endpoint da API",
                apiEndpointHint: "Deixe em branco para usar o padrão, se houver suporte.",
                modelNameLabel: "Nome do modelo",
                modelHint: "Defina o identificador do modelo usado pelo seu provedor.",
                timeoutLabel: "Tempo limite (segundos)",
                retryLabel: "Máximo de tentativas",
                defaultNotesTitle: "Notas do cliente padrão",
                defaultNotesLead: "<strong>O cliente simulado padrão</strong> é útil para demos locais e testes de UI.",
                defaultNoteOne: "Nenhuma chave de API é necessária",
                defaultNoteTwo: "Seguro para experimentação local",
                defaultNoteThree: "Provedores reais continuam opcionais",
                testConnection: "Testar conexão",
                saveConfig: "Salvar configuração",
                configStatusLabel: "Status:",
                configProviderLabel: "Fornecedor:",
                agentLabEyebrow: "Sistema de design do agente",
                agentLabHeader: "Estúdio do Agente",
                agentLabDesc: "Prototipe o agente de análise, o ciclo de revisão do fluxo e a superfície de engenharia de prompts em um só lugar.",
                studioMetricOneLabel: "Profundidade de análise",
                studioMetricOneValue: "5 camadas",
                studioMetricTwoLabel: "Escopo de otimização",
                studioMetricTwoValue: "Lance / Orçamento / Consulta",
                studioMetricThreeLabel: "Modo Prompt",
                studioMetricThreeValue: "Estruturado",
                runObjectiveTitle: "Objetivo de execução",
                objectiveLabel: "Objetivo",
                objectiveDefault: "Melhorar a eficiência da campanha enquanto protege o crescimento lucrativo.",
                runAgent: "Executar agente",
                promptTemplateTitle: "Modelo de prompt",
                systemRoleLabel: "Papel do sistema",
                taskTemplateLabel: "Modelo de tarefa",
                outputStyleLabel: "Estilo de saída",
                reloadTemplate: "Recarregar modelo",
                saveTemplate: "Salvar modelo",
                agentOutputTitle: "Saída do agente",
                workflowSteps: "Etapas do fluxo",
                agentStepsEmpty: "Execute o agente para revisar as etapas do fluxo.",
                findings: "Achados",
                findingsEmpty: "Ainda não há achados.",
                recommendations: "Recomendações",
                recommendationsEmpty: "Ainda não há recomendações.",
                promptPreview: "Pré-visualização do prompt",
                promptEmpty: "Ainda não há prompt renderizado.",
                llmOutput: "Saída do LLM",
                llmEmpty: "Ainda não há saída do modelo.",
                nextActions: "Próximas ações",
                nextActionsEmpty: "Ainda não há próximas ações.",
                cancel: "Cancelar",
                save: "Salvar",
                pageChat: "Central de comando",
                pageUsers: "Entidades",
                pageStats: "Painel de insights",
                pageLlm: "Configuração LLM",
                pageAgentLab: "Estúdio do Agente",
                statusActive: "Ativo",
                statusInactive: "Inativo",
                statusDeleted: "Excluído",
                serviceOnline: "Serviço online",
                serviceChecking: "Verificando..."
            },
            ja: {
                ...en,
                brandTitle: "エージェントコンソール",
                workspaceTitle: "ワークスペース",
                settingsTitle: "設定",
                navChat: "コマンドセンター",
                navChatHint: "概要とガイド付きチャット",
                navUsers: "エンティティ",
                navUsersHint: "ユーザーと運用担当者",
                navStats: "インサイト",
                navStatsHint: "リアルタイム指標とチャート",
                navAgentLab: "エージェントスタジオ",
                navAgentLabHint: "ワークフローとプロンプト設計",
                navLlm: "LLM 設定",
                navLlmHint: "プロバイダーとモデル設定",
                serviceStatusLabel: "サービス状態",
                statusPill: "自動化の準備完了",
                topEyebrow: "インテリジェント運用ダッシュボード",
                clearChat: "チャットを消去",
                refresh: "更新",
                heroTag: "Amazon Ads エージェントシステム",
                heroTitle: "検索語分析からキャンペーン最適化までを一つの画面で。",
                heroDesc: "広告分析、推奨、入札最適化、プロンプト駆動ワークフローを扱うエージェントを構築できます。",
                heroPrimary: "スタジオを開く",
                heroSecondary: "インサイトを見る",
                heroVisualTitle: "最適化シグナル",
                heroVisualTrend: "効率 +18%",
                metricCtr: "CTR",
                metricAcos: "ACOS",
                metricRoas: "ROAS",
                overviewOneTitle: "検索語分析",
                overviewOneDesc: "価値の高い検索語を捉え、無駄を切り分け、再利用可能なインサイトを推奨ループへ戻します。",
                overviewTwoTitle: "自動最適化",
                overviewTwoDesc: "診断結果を予算調整、入札最適化、除外キーワード提案に変換します。",
                overviewThreeTitle: "Prompt ワークフロー",
                overviewThreeDesc: "構造化プロンプトを設計し、再利用可能な広告分析フローへ組み立てます。",
                chatPlaceholder: "コマンドを入力。Enter で送信、Shift + Enter で改行。",
                sendMessageAria: "メッセージを送信",
                languageSelectorAria: "言語セレクター",
                quickPrompts: "クイックプロンプト:",
                entityBannerEyebrow: "運用データレイヤー",
                entityBannerTitle: "キャンペーン判断を支える人と役割を管理します。",
                entityBannerMetricOne: "アクティブ担当者",
                entityBannerMetricTwo: "ワークフロー適用率",
                userSearchPlaceholder: "将来のフィルタ用に予約された検索欄",
                filterAllStatuses: "すべての状態",
                addUser: "ユーザー追加",
                tableUserId: "ユーザー ID",
                tableUsername: "ユーザー名",
                tableEmail: "メール",
                tablePhone: "電話番号",
                tableStatus: "状態",
                tableCreated: "作成日",
                tableActions: "操作",
                loadingUsers: "ユーザーを読み込み中...",
                previous: "前へ",
                page: "ページ",
                next: "次へ",
                insightEyebrow: "インサイトボード",
                insightTitle: "アカウント健全性とワークフロー成熟度をより明確に把握できます。",
                insightSparklineLabel: "ワークフロー信頼度の推移",
                totalUsers: "総ユーザー数",
                activeUsers: "アクティブユーザー",
                inactiveUsers: "非アクティブユーザー",
                deletedUsers: "削除済みユーザー",
                statusDistribution: "状態分布",
                statusDistributionNote: "バックエンド統計と同期",
                agentCoverageTitle: "エージェント適用範囲",
                agentCoverageNote: "可視化された計画レイヤー",
                donutCenterLabel: "マップ済み",
                legendOne: "分析",
                legendTwo: "最適化",
                legendThree: "ワークフロー",
                llmEyebrow: "モデル運用",
                llmHeader: "LLM 設定",
                llmDesc: "エージェント分析機能で使用する任意のモデルプロバイダーを設定します。",
                providerCardTitle: "プロバイダー",
                enableLlm: "LLM 連携を有効化",
                providerLabel: "プロバイダー",
                providerDefault: "デフォルトのモッククライアント",
                providerCustom: "カスタム API",
                providerBadgeDefault: "標準",
                apiSettingsTitle: "API 設定",
                apiKeyLabel: "API キー *",
                apiKeyPlaceholder: "API キーを入力",
                apiKeyHint: "ここにプロバイダーのキーを貼り付けます。",
                apiEndpointLabel: "API エンドポイント",
                apiEndpointHint: "対応していれば空欄で既定値を利用します。",
                modelNameLabel: "モデル名",
                modelHint: "プロバイダーで使うモデル識別子を設定します。",
                timeoutLabel: "タイムアウト（秒）",
                retryLabel: "最大再試行回数",
                defaultNotesTitle: "デフォルトクライアントのメモ",
                defaultNotesLead: "<strong>デフォルトのモッククライアント</strong> はローカルデモや UI テストに便利です。",
                defaultNoteOne: "API キー不要",
                defaultNoteTwo: "ローカル実験に安全",
                defaultNoteThree: "実際のプロバイダーは引き続き任意です",
                testConnection: "接続テスト",
                saveConfig: "設定を保存",
                configStatusLabel: "状態:",
                configProviderLabel: "プロバイダー:",
                agentLabEyebrow: "エージェント設計システム",
                agentLabHeader: "エージェントスタジオ",
                agentLabDesc: "分析エージェント、レビュー・ループ、プロンプト設計画面を一か所で試作できます。",
                studioMetricOneLabel: "分析深度",
                studioMetricOneValue: "5 レイヤー",
                studioMetricTwoLabel: "最適化範囲",
                studioMetricTwoValue: "入札 / 予算 / 検索語",
                studioMetricThreeLabel: "Prompt モード",
                studioMetricThreeValue: "構造化",
                runObjectiveTitle: "実行目的",
                objectiveLabel: "目的",
                objectiveDefault: "利益成長を守りながら、キャンペーン効率を改善する。",
                runAgent: "エージェントを実行",
                promptTemplateTitle: "Prompt テンプレート",
                systemRoleLabel: "システムロール",
                taskTemplateLabel: "タスクテンプレート",
                outputStyleLabel: "出力スタイル",
                reloadTemplate: "テンプレートを再読み込み",
                saveTemplate: "テンプレートを保存",
                agentOutputTitle: "エージェント出力",
                workflowSteps: "ワークフロー手順",
                agentStepsEmpty: "エージェントを実行するとワークフロー手順を確認できます。",
                findings: "検出事項",
                findingsEmpty: "まだ検出事項はありません。",
                recommendations: "推奨事項",
                recommendationsEmpty: "まだ推奨事項はありません。",
                promptPreview: "Prompt プレビュー",
                promptEmpty: "まだ Prompt は生成されていません。",
                llmOutput: "LLM 出力",
                llmEmpty: "まだモデル出力はありません。",
                nextActions: "次のアクション",
                nextActionsEmpty: "まだ次のアクションはありません。",
                cancel: "キャンセル",
                save: "保存",
                pageChat: "コマンドセンター",
                pageUsers: "エンティティ",
                pageStats: "インサイト",
                pageLlm: "LLM 設定",
                pageAgentLab: "エージェントスタジオ",
                statusActive: "有効",
                statusInactive: "無効",
                statusDeleted: "削除済み",
                serviceOnline: "サービス稼働中",
                serviceChecking: "確認中..."
            },
            ar: {
                ...en,
                brandTitle: "لوحة الوكيل",
                workspaceTitle: "مساحة العمل",
                settingsTitle: "الإعدادات",
                navChat: "مركز القيادة",
                navChatHint: "نظرة عامة ومحادثة موجهة",
                navUsers: "الكيانات",
                navUsersHint: "المستخدمون والمشغلون",
                navStats: "لوحة الرؤى",
                navStatsHint: "مقاييس ورسوم بيانية",
                navAgentLab: "استوديو الوكيل",
                navAgentLabHint: "سير العمل وتصميم الموجهات",
                navLlm: "إعداد LLM",
                navLlmHint: "المزوّد والنموذج",
                serviceStatusLabel: "حالة الخدمة",
                statusPill: "الأتمتة جاهزة",
                topEyebrow: "لوحة تشغيل ذكية",
                clearChat: "مسح المحادثة",
                refresh: "تحديث",
                heroTag: "نظام وكيل Amazon Ads",
                heroTitle: "من تحليل عبارات البحث إلى تحسين الحملات في مساحة واحدة.",
                heroDesc: "أنشئ وكيلاً لتحليل الإعلانات واقتراح الإجراءات وتحسين العروض وسير العمل المعتمد على الموجهات.",
                heroPrimary: "فتح الاستوديو",
                heroSecondary: "عرض اللوحة",
                heroVisualTitle: "إشارة التحسين",
                heroVisualTrend: "+18% كفاءة",
                metricCtr: "CTR",
                metricAcos: "ACOS",
                metricRoas: "ROAS",
                overviewOneTitle: "تحليل عبارات البحث",
                overviewOneDesc: "التقط الكلمات المهمة، اعزل الهدر، وأعد استخدام الرؤى داخل دورة التوصيات.",
                overviewTwoTitle: "تحسين تلقائي",
                overviewTwoDesc: "حوّل التشخيصات إلى تعديلات على الميزانية والعروض والكلمات السلبية مع ضوابط حماية.",
                overviewThreeTitle: "سير عمل Prompt",
                overviewThreeDesc: "صمّم موجهات منظمة واربطها في مسارات قابلة لإعادة الاستخدام لتحليل الإعلانات.",
                chatPlaceholder: "اكتب أمراً. Enter للإرسال و Shift + Enter لسطر جديد.",
                sendMessageAria: "إرسال الرسالة",
                languageSelectorAria: "محدد اللغة",
                quickPrompts: "أوامر سريعة:",
                entityBannerEyebrow: "طبقة التشغيل",
                entityBannerTitle: "إدارة الأشخاص وراء قرارات الحملات.",
                entityBannerMetricOne: "المشغلون النشطون",
                entityBannerMetricTwo: "تغطية سير العمل",
                userSearchPlaceholder: "حقل البحث مخصص للفلاتر القادمة",
                filterAllStatuses: "كل الحالات",
                addUser: "إضافة مستخدم",
                tableUserId: "معرّف المستخدم",
                tableUsername: "اسم المستخدم",
                tableEmail: "البريد الإلكتروني",
                tablePhone: "الهاتف",
                tableStatus: "الحالة",
                tableCreated: "تاريخ الإنشاء",
                tableActions: "الإجراءات",
                loadingUsers: "جارٍ تحميل المستخدمين...",
                previous: "السابق",
                page: "الصفحة",
                next: "التالي",
                insightEyebrow: "لوحة الرؤى",
                insightTitle: "رؤية أوضح لصحة الحساب ونضج سير العمل.",
                insightSparklineLabel: "اتجاه ثقة سير العمل",
                totalUsers: "إجمالي المستخدمين",
                activeUsers: "المستخدمون النشطون",
                inactiveUsers: "المستخدمون غير النشطين",
                deletedUsers: "المستخدمون المحذوفون",
                statusDistribution: "توزيع الحالات",
                statusDistributionNote: "متزامن مع إحصاءات الخلفية",
                agentCoverageTitle: "تغطية الوكيل",
                agentCoverageNote: "طبقة تخطيط مرئية",
                donutCenterLabel: "مربوط",
                legendOne: "تحليل",
                legendTwo: "تحسين",
                legendThree: "سير العمل",
                llmEyebrow: "تشغيل النموذج",
                llmHeader: "إعداد LLM",
                llmDesc: "اضبط مزوّد النموذج الاختياري المستخدم في ميزات تحليل الوكيل.",
                providerCardTitle: "المزوّد",
                enableLlm: "تفعيل تكامل LLM",
                providerLabel: "المزوّد",
                providerDefault: "عميل افتراضي تجريبي",
                providerCustom: "واجهة API مخصصة",
                providerBadgeDefault: "افتراضي",
                apiSettingsTitle: "إعدادات API",
                apiKeyLabel: "API Key *",
                apiKeyPlaceholder: "أدخل API Key",
                apiKeyHint: "ألصق مفتاح المزوّد هنا.",
                apiEndpointLabel: "عنوان API",
                apiEndpointHint: "اتركه فارغاً لاستخدام الإعداد الافتراضي إذا كان مدعوماً.",
                modelNameLabel: "اسم النموذج",
                modelHint: "حدّد معرّف النموذج المستخدم من مزوّدك.",
                timeoutLabel: "مهلة الانتظار (ثانية)",
                retryLabel: "أقصى عدد لإعادة المحاولة",
                defaultNotesTitle: "ملاحظات العميل الافتراضي",
                defaultNotesLead: "<strong>العميل التجريبي الافتراضي</strong> مفيد للعروض المحلية واختبار الواجهة.",
                defaultNoteOne: "لا يحتاج إلى API Key",
                defaultNoteTwo: "آمن للتجارب المحلية",
                defaultNoteThree: "المزوّدون الحقيقيون ما زالوا اختياريين",
                testConnection: "اختبار الاتصال",
                saveConfig: "حفظ الإعداد",
                configStatusLabel: "الحالة:",
                configProviderLabel: "المزوّد:",
                agentLabEyebrow: "نظام تصميم الوكيل",
                agentLabHeader: "استوديو الوكيل",
                agentLabDesc: "صمّم نموذج وكيل التحليل وسير عمل المراجعة وهندسة الموجهات في مكان واحد.",
                studioMetricOneLabel: "عمق التحليل",
                studioMetricOneValue: "5 طبقات",
                studioMetricTwoLabel: "نطاق التحسين",
                studioMetricTwoValue: "العرض / الميزانية / الاستعلام",
                studioMetricThreeLabel: "وضع Prompt",
                studioMetricThreeValue: "منظم",
                runObjectiveTitle: "هدف التشغيل",
                objectiveLabel: "الهدف",
                objectiveDefault: "تحسين كفاءة الحملة مع الحفاظ على النمو المربح.",
                runAgent: "تشغيل الوكيل",
                promptTemplateTitle: "قالب Prompt",
                systemRoleLabel: "دور النظام",
                taskTemplateLabel: "قالب المهمة",
                outputStyleLabel: "أسلوب الإخراج",
                reloadTemplate: "إعادة تحميل القالب",
                saveTemplate: "حفظ القالب",
                agentOutputTitle: "نتائج تشغيل الوكيل",
                workflowSteps: "خطوات سير العمل",
                agentStepsEmpty: "شغّل الوكيل لمراجعة خطوات سير العمل.",
                findings: "النتائج",
                findingsEmpty: "لا توجد نتائج بعد.",
                recommendations: "التوصيات",
                recommendationsEmpty: "لا توجد توصيات بعد.",
                promptPreview: "معاينة Prompt",
                promptEmpty: "لم يتم إنشاء Prompt بعد.",
                llmOutput: "مخرجات LLM",
                llmEmpty: "لا توجد مخرجات للنموذج بعد.",
                nextActions: "الإجراءات التالية",
                nextActionsEmpty: "لا توجد إجراءات تالية بعد.",
                cancel: "إلغاء",
                save: "حفظ",
                pageChat: "مركز القيادة",
                pageUsers: "الكيانات",
                pageStats: "لوحة الرؤى",
                pageLlm: "إعداد LLM",
                pageAgentLab: "استوديو الوكيل",
                statusActive: "نشط",
                statusInactive: "غير نشط",
                statusDeleted: "محذوف",
                serviceOnline: "الخدمة متصلة",
                serviceOffline: "فشل الاتصال",
                serviceChecking: "جارٍ التحقق..."
            }
        });

        return {
            en,
            zh: { ...en, ...zh },
            es: { ...en, ...packs.es },
            fr: { ...en, ...packs.fr },
            de: { ...en, ...packs.de },
            pt: { ...en, ...packs.pt },
            ja: { ...en, ...packs.ja },
            ar: { ...en, ...packs.ar }
        };
    }

    init() {
        this.populateLanguageSelector();
        this.bindEvents();
        this.applyTranslations();
        this.renderWelcomeMessage();
        this.checkHealth();
    }

    bindEvents() {
        document.querySelectorAll(".nav-item[data-view]").forEach((item) => {
            item.addEventListener("click", (e) => {
                e.preventDefault();
                this.switchView(item.dataset.view);
            });
        });

        document.querySelectorAll("[data-target-view]").forEach((button) => {
            button.addEventListener("click", () => this.switchView(button.dataset.targetView));
        });

        document.getElementById("languageSelect").addEventListener("change", (e) => this.setLanguage(e.target.value));
        document.getElementById("sendBtn").addEventListener("click", () => this.sendMessage());
        document.getElementById("chatInput").addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        document.getElementById("chatInput").addEventListener("input", (e) => {
            e.target.style.height = "auto";
            e.target.style.height = `${Math.min(e.target.scrollHeight, 180)}px`;
        });

        document.getElementById("agentObjective").addEventListener("input", () => {
            this.objectiveTouched = true;
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

        document.getElementById("userSearch").addEventListener("input", this.debounce(() => {
            this.currentPage = 1;
            this.loadUsers();
        }, 300));

        document.querySelectorAll(".page-btn").forEach((btn) => {
            btn.addEventListener("click", () => {
                if (btn.dataset.page === "prev" && this.currentPage > 1) {
                    this.currentPage -= 1;
                    this.loadUsers();
                } else if (btn.dataset.page === "next") {
                    this.currentPage += 1;
                    this.loadUsers();
                }
            });
        });

        document.getElementById("llmProvider").addEventListener("change", () => this.updateProviderUI());
        document.getElementById("saveConfigBtn").addEventListener("click", () => this.saveLLMConfig());
        document.getElementById("testConnectionBtn").addEventListener("click", () => this.testLLMConnection());
        document.getElementById("runAgentBtn").addEventListener("click", () => this.runAgentWorkflow());
        document.getElementById("reloadPromptBtn").addEventListener("click", () => this.loadPromptTemplate());
        document.getElementById("savePromptBtn").addEventListener("click", () => this.savePromptTemplate());
    }

    t(key) {
        return this.translations[this.currentLanguage]?.[key] || this.translations.en[key] || key;
    }

    getLocale() {
        return this.languageOptions.find((item) => item.code === this.currentLanguage)?.locale || "en-US";
    }

    populateLanguageSelector() {
        const select = document.getElementById("languageSelect");
        select.innerHTML = this.languageOptions.map((item) => `<option value="${item.code}">${item.label}</option>`).join("");
        if (!this.languageOptions.find((item) => item.code === this.currentLanguage)) {
            this.currentLanguage = "en";
        }
        select.value = this.currentLanguage;
    }

    setLanguage(language) {
        if (!this.languageOptions.find((item) => item.code === language)) {
            language = "en";
        }
        this.currentLanguage = language;
        localStorage.setItem("agent-ui-language", this.currentLanguage);
        this.applyTranslations();
        this.updateViewTitle();
        this.renderWelcomeMessageIfNeeded();
        this.renderLocalizedDynamicContent();
        this.renderStoredStats();
    }

    applyTranslations() {
        document.documentElement.lang = this.currentLanguage === "zh" ? "zh-CN" : this.currentLanguage;
        document.documentElement.dir = "ltr";

        document.querySelectorAll("[data-i18n]").forEach((el) => {
            const value = this.t(el.dataset.i18n);
            el.setAttribute("dir", this.currentLanguage === "ar" ? "auto" : "ltr");
            if (typeof value === "string" && value.includes("<strong>")) {
                el.innerHTML = value;
            } else {
                el.textContent = value;
            }
        });

        document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
            el.placeholder = this.t(el.dataset.i18nPlaceholder);
        });

        document.querySelectorAll("[data-i18n-aria-label]").forEach((el) => {
            el.setAttribute("aria-label", this.t(el.dataset.i18nAriaLabel));
        });

        const objectiveEl = document.getElementById("agentObjective");
        if (!this.objectiveTouched || this.matchesAnyObjectiveDefault(objectiveEl.value)) {
            objectiveEl.value = this.t("objectiveDefault");
        }

        document.title = this.currentLanguage === "zh" ? "Amazon Ads 智能体控制台" : this.t("brandTitle");
        document.getElementById("currentLanguageLabel").textContent = this.languageOptions.find((item) => item.code === this.currentLanguage)?.badge || "EN";
        document.getElementById("languageSelect").value = this.currentLanguage;
        [".page-title", ".status-text", "#currentStatus", "#currentProvider", "#agentSteps", "#agentFindings", "#agentRecommendations", "#agentPrompt", "#agentLlmOutput", "#agentNextActions"]
            .forEach((selector) => {
                const el = document.querySelector(selector);
                if (el) {
                    el.setAttribute("dir", this.currentLanguage === "ar" ? "auto" : "ltr");
                }
            });
        this.updateProviderUI();
        this.renderHealthStatus();
    }

    matchesAnyObjectiveDefault(value) {
        return Object.values(this.translations).some((pack) => pack.objectiveDefault === value);
    }

    renderWelcomeMessageIfNeeded() {
        const container = document.getElementById("chatMessages");
        if (container.children.length === 1 && container.querySelector(".message.assistant")) {
            this.renderWelcomeMessage();
        }
    }

    renderWelcomeMessage() {
        document.getElementById("chatMessages").innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">AI</div>
                <div class="message-content">
                    <div class="message-text">
                        ${this.t("welcomeTitle")}
                        <ul>
                            <li>${this.t("welcomeLineOne")}</li>
                            <li>${this.t("welcomeLineTwo")}</li>
                            <li>${this.t("welcomeLineThree")}</li>
                            <li>${this.t("welcomeLineFour")}</li>
                        </ul>
                        ${this.t("welcomeFooter")}
                    </div>
                    <div class="message-time">${this.formatClock()}</div>
                </div>
            </div>
        `;
    }

    renderLocalizedDynamicContent() {
        if (this.currentView === "users") {
            this.renderUsers(this.lastUsers);
        }

        if (this.lastStats) {
            this.renderStoredStats();
        }

        if (this.lastLLMConfig) {
            this.applyLLMConfig(this.lastLLMConfig.enabled, this.lastLLMConfig.config);
        }

        if (this.lastAgentRun) {
            this.renderAgentRun(this.lastAgentRun, false);
        }

        document.getElementById("modalTitle").textContent = this.editingUserId ? this.t("modalEditUser") : this.t("modalAddUser");
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();
            this.lastHealthState = data.status === "healthy" ? "online" : "offline";
            this.renderHealthStatus();
        } catch (error) {
            this.lastHealthState = "offline";
            this.renderHealthStatus();
        }
    }

    renderHealthStatus() {
        const statusDot = document.querySelector(".status-dot");
        const statusText = document.querySelector(".status-text");
        if (!statusDot || !statusText) return;

        statusDot.classList.toggle("online", this.lastHealthState === "online");
        statusText.textContent = this.lastHealthState === "online"
            ? this.t("serviceOnline")
            : this.lastHealthState === "offline"
                ? this.t("serviceOffline")
                : this.t("serviceChecking");
    }

    switchView(view) {
        this.currentView = view;
        document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
        document.querySelector(`.nav-item[data-view="${view}"]`).classList.add("active");
        document.querySelectorAll(".content-area").forEach((area) => area.classList.add("hidden"));
        document.getElementById(`${this.getViewId(view)}View`).classList.remove("hidden");
        this.updateViewTitle();

        if (view === "users") this.loadUsers();
        if (view === "stats") this.loadStatistics();
        if (view === "llm-config") this.loadLLMConfig();
        if (view === "agent-lab") this.loadPromptTemplate();
    }

    updateViewTitle() {
        const titleMap = {
            chat: this.t("pageChat"),
            users: this.t("pageUsers"),
            stats: this.t("pageStats"),
            "llm-config": this.t("pageLlm"),
            "agent-lab": this.t("pageAgentLab")
        };
        document.querySelector(".page-title").textContent = titleMap[this.currentView] || this.t("pageChat");
    }

    getViewId(view) {
        return {
            chat: "chat",
            users: "users",
            stats: "stats",
            "llm-config": "llmConfig",
            "agent-lab": "agentLab"
        }[view] || view;
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
            this.addMessage(this.t("chatRequestFailed"), "assistant");
        }
    }

    addMessage(text, role, data = null) {
        const container = document.getElementById("chatMessages");
        const messageEl = document.createElement("div");
        messageEl.className = `message ${role}`;
        let contentText = text;
        if (data?.users) {
            contentText += "\n\n";
            data.users.slice(0, 5).forEach((user) => {
                contentText += `- ${user.username} (${user.email})\n`;
            });
        }
        if (data?.statistics) {
            const active = data.statistics.status_distribution?.active || 0;
            const inactive = data.statistics.status_distribution?.inactive || 0;
            const deleted = data.statistics.status_distribution?.deleted || 0;
            contentText += `\n\n${this.t("statusActive")}: ${active}\n${this.t("statusInactive")}: ${inactive}\n${this.t("statusDeleted")}: ${deleted}`;
        }
        messageEl.innerHTML = `
            <div class="message-avatar">${role === "user" ? "U" : "AI"}</div>
            <div class="message-content">
                <div class="message-text">${contentText.replace(/\n/g, "<br>")}</div>
                <div class="message-time">${this.formatClock()}</div>
            </div>
        `;
        container.appendChild(messageEl);
        container.scrollTop = container.scrollHeight;
    }

    clearChat() {
        document.getElementById("chatMessages").innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">AI</div>
                <div class="message-content">
                    <div class="message-text">${this.t("clearedChat")}</div>
                    <div class="message-time">${this.formatClock()}</div>
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
            this.lastUsers = data.users || [];
            this.renderUsers(this.lastUsers);
            document.getElementById("currentPage").textContent = this.currentPage;
        } catch (error) {
            this.showToast(this.t("toastLoadUsersFailed"), "error");
        }
    }

    renderUsers(users) {
        const tbody = document.getElementById("usersTableBody");
        if (!users.length) {
            tbody.innerHTML = `<tr><td colspan="7" class="loading-text">${this.t("noUsersFound")}</td></tr>`;
            return;
        }
        tbody.innerHTML = users.map((user) => `
            <tr>
                <td><code style="font-size:12px">${user.user_id.substring(0, 8)}...</code></td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.phone || "-"}</td>
                <td><span class="status-badge ${user.status}">${this.getStatusText(user.status)}</span></td>
                <td>${this.formatDate(user.created_at)}</td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn" onclick="agentUI.editUser('${user.user_id}')">${this.t("actionEdit")}</button>
                        <button class="action-btn danger" onclick="agentUI.deleteUser('${user.user_id}')">${this.t("actionDelete")}</button>
                    </div>
                </td>
            </tr>
        `).join("");
    }

    getStatusText(status) {
        return {
            active: this.t("statusActive"),
            inactive: this.t("statusInactive"),
            deleted: this.t("statusDeleted")
        }[status] || status;
    }

    formatDate(timestamp) {
        if (!timestamp) return "-";
        return new Date(timestamp).toLocaleDateString(this.getLocale());
    }

    formatClock() {
        return new Date().toLocaleTimeString(this.getLocale(), { hour: "2-digit", minute: "2-digit" });
    }

    async editUser(userId) {
        try {
            const response = await fetch(`${this.apiBase}/users/${userId}`);
            const user = await response.json();
            this.editingUserId = userId;
            document.getElementById("modalTitle").textContent = this.t("modalEditUser");
            const form = document.getElementById("userForm");
            form.username.value = user.username;
            form.email.value = user.email;
            form.phone.value = user.phone || "";
            form.status.value = user.status;
            form.tags.value = (user.tags || []).join(", ");
            this.showUserModal();
        } catch (error) {
            this.showToast(this.t("toastLoadUserDetailsFailed"), "error");
        }
    }

    async deleteUser(userId) {
        if (!confirm(this.t("toastDeleteConfirm"))) return;
        try {
            const response = await fetch(`${this.apiBase}/users/${userId}`, { method: "DELETE" });
            const data = await response.json();
            if (data.success) {
                this.showToast(this.t("toastUserDeleted"), "success");
                this.loadUsers();
            } else {
                this.showToast(data.error || this.t("toastDeleteFailed"), "error");
            }
        } catch (error) {
            this.showToast(this.t("toastDeleteFailed"), "error");
        }
    }

    showUserModal() {
        document.getElementById("userModal").classList.add("show");
    }

    hideUserModal() {
        document.getElementById("userModal").classList.remove("show");
        document.getElementById("userForm").reset();
        this.editingUserId = null;
        document.getElementById("modalTitle").textContent = this.t("modalAddUser");
    }

    async submitUserForm() {
        const form = document.getElementById("userForm");
        const formData = new FormData(form);
        const userData = {
            username: formData.get("username"),
            email: formData.get("email"),
            phone: formData.get("phone") || null,
            status: formData.get("status"),
            tags: formData.get("tags") ? formData.get("tags").split(",").map((tag) => tag.trim()).filter(Boolean) : []
        };
        try {
            const response = await fetch(`${this.apiBase}/users${this.editingUserId ? `/${this.editingUserId}` : ""}`, {
                method: this.editingUserId ? "PUT" : "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData)
            });
            const data = await response.json();
            if (data.success) {
                this.showToast(this.editingUserId ? this.t("toastUserUpdated") : this.t("toastUserCreated"), "success");
                this.hideUserModal();
                this.loadUsers();
            } else {
                this.showToast(data.error || this.t("toastOperationFailed"), "error");
            }
        } catch (error) {
            this.showToast(this.t("toastOperationFailed"), "error");
        }
    }

    async loadStatistics() {
        try {
            const response = await fetch(`${this.apiBase}/statistics`);
            this.lastStats = await response.json();
            this.renderStoredStats();
        } catch (error) {
            this.showToast(this.t("toastLoadStatisticsFailed"), "error");
        }
    }

    renderStoredStats() {
        if (!this.lastStats) return;
        const totals = {
            total: this.lastStats.total_users || 0,
            active: this.lastStats.status_distribution?.active || 0,
            inactive: this.lastStats.status_distribution?.inactive || 0,
            deleted: this.lastStats.status_distribution?.deleted || 0
        };
        document.getElementById("totalUsers").textContent = totals.total;
        document.getElementById("activeUsers").textContent = totals.active;
        document.getElementById("inactiveUsers").textContent = totals.inactive;
        document.getElementById("deletedUsers").textContent = totals.deleted;
        document.getElementById("entityBannerActive").textContent = totals.active;
        document.getElementById("entityBannerCoverage").textContent = `${Math.round(((totals.active + totals.inactive) / Math.max(totals.total, 1)) * 100)}%`;
        const maxCount = Math.max(totals.active, totals.inactive, totals.deleted, 1);
        document.querySelectorAll(".chart-bar").forEach((bar) => {
            const count = totals[bar.dataset.status] || 0;
            bar.querySelector(".bar-fill").style.width = `${(count / maxCount) * 100}%`;
            bar.querySelector(".bar-value").textContent = count;
        });
    }

    refreshCurrentView() {
        const activeView = document.querySelector(".content-area:not(.hidden)")?.id;
        if (activeView === "usersView") this.loadUsers();
        else if (activeView === "statsView") this.loadStatistics();
        else if (activeView === "llmConfigView") this.loadLLMConfig();
        else if (activeView === "agentLabView") this.loadPromptTemplate();
        else this.checkHealth();
        this.showToast(this.t("toastViewRefreshed"), "success");
    }

    showToast(message, type = "info") {
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.getElementById("toastContainer").appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
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
            this.lastLLMConfig = { enabled: data.enabled || false, config };
            this.applyLLMConfig(this.lastLLMConfig.enabled, config);
        } catch (error) {
            this.showToast(this.t("toastLoadConfigFailed"), "error");
        }
    }

    applyLLMConfig(enabled, config = {}) {
        document.getElementById("llmEnabled").checked = enabled;
        document.getElementById("llmProvider").value = (config.provider || "mock") === "mock" ? "default" : (config.provider || "default");
        document.getElementById("llmApiKey").value = config.api_key || "";
        document.getElementById("llmApiEndpoint").value = config.api_endpoint || "";
        document.getElementById("llmModel").value = config.model || "";
        document.getElementById("llmTimeout").value = config.timeout || 30;
        document.getElementById("llmMaxRetries").value = config.max_retries || 3;
        this.updateProviderUI();
        this.updateStatusDisplay(enabled, config.provider || "mock");
    }

    updateProviderUI() {
        const provider = document.getElementById("llmProvider").value;
        const apiConfigCard = document.getElementById("apiConfigCard");
        const defaultModelInfo = document.getElementById("defaultModelInfo");
        document.getElementById("providerBadge").textContent = {
            default: this.t("providerBadgeDefault"),
            openai: "OpenAI",
            pangu: "Pangu",
            custom: this.t("providerCustom")
        }[provider] || provider;
        if (provider === "default") {
            defaultModelInfo.style.display = "block";
            apiConfigCard.style.display = "none";
            return;
        }
        defaultModelInfo.style.display = "none";
        apiConfigCard.style.display = "block";
        const prefix = provider === "openai" ? "openai" : provider === "pangu" ? "pangu" : "custom";
        document.getElementById("llmApiEndpoint").placeholder = this.t(`${prefix}EndpointPlaceholder`);
        document.getElementById("llmModel").placeholder = this.t(`${prefix}ModelPlaceholder`);
        document.getElementById("apiKeyHint").textContent = this.t(`${prefix}ApiHint`);
    }

    updateStatusDisplay(enabled, provider) {
        const statusEl = document.getElementById("currentStatus");
        statusEl.textContent = enabled ? this.t("statusEnabled") : this.t("statusDisabled");
        statusEl.style.color = enabled ? "#5ae7a5" : "#ff7b7b";
        document.getElementById("currentProvider").textContent = {
            mock: this.t("defaultProviderName"),
            openai: "OpenAI",
            pangu: "Pangu",
            custom: this.t("providerCustom")
        }[provider] || provider;
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
            this.showToast(this.t("toastApiKeyRequired"), "error");
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
                this.showToast(this.t("toastConfigSaved"), "success");
                this.lastLLMConfig = { enabled: config.enabled, config: { ...config } };
                this.updateStatusDisplay(config.enabled, actualProvider);
            } else {
                this.showToast(data.error || this.t("toastSaveFailed"), "error");
            }
        } catch (error) {
            this.showToast(this.t("toastSaveFailed"), "error");
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
            this.showToast(this.t("toastTestingConnection"), "info");
            const response = await fetch(`${this.apiBase}/config/llm/test`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(config)
            });
            const data = await response.json();
            this.showToast(data.success ? (data.message || this.t("toastConnectionSucceeded")) : (data.error || this.t("toastConnectionFailed")), data.success ? "success" : "error");
        } catch (error) {
            this.showToast(this.t("toastConnectionTestFailed"), "error");
        }
    }

    async loadPromptTemplate() {
        try {
            const response = await fetch(`${this.apiBase}/ad-agent/prompt-template`);
            const data = await response.json();
            if (!data.success) {
                this.showToast(data.error || this.t("toastLoadPromptFailed"), "error");
                return;
            }
            const template = data.template || {};
            document.getElementById("promptSystemRole").value = template.system_role || "";
            document.getElementById("promptTaskTemplate").value = template.task_template || "";
            document.getElementById("promptOutputStyle").value = template.output_style || "";
        } catch (error) {
            this.showToast(this.t("toastLoadPromptFailed"), "error");
        }
    }

    async savePromptTemplate() {
        try {
            const response = await fetch(`${this.apiBase}/ad-agent/prompt-template`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    system_role: document.getElementById("promptSystemRole").value,
                    task_template: document.getElementById("promptTaskTemplate").value,
                    output_style: document.getElementById("promptOutputStyle").value
                })
            });
            const data = await response.json();
            this.showToast(data.success ? this.t("toastPromptSaved") : (data.error || this.t("toastSavePromptFailed")), data.success ? "success" : "error");
        } catch (error) {
            this.showToast(this.t("toastSavePromptFailed"), "error");
        }
    }

    async runAgentWorkflow() {
        const objective = document.getElementById("agentObjective").value.trim();
        if (!objective) {
            this.showToast(this.t("toastObjectiveRequired"), "error");
            return;
        }
        try {
            this.showToast(this.t("toastRunningAgent"), "info");
            const response = await fetch(`${this.apiBase}/ad-agent/run`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ objective })
            });
            const data = await response.json();
            if (!data.success) {
                this.showToast(data.error || this.t("toastAgentRunFailed"), "error");
                return;
            }
            this.renderAgentRun(data.run);
            this.showToast(this.t("toastAgentCompleted"), "success");
        } catch (error) {
            this.showToast(this.t("toastAgentRunFailed"), "error");
        }
    }

    renderAgentRun(run = {}, persist = true) {
        if (persist) {
            this.lastAgentRun = run;
        }
        document.getElementById("agentSteps").innerHTML = (run.steps || []).map((step) => `<div><strong>${step.name}</strong> [${this.getWorkflowStatusLabel(step.status)}]<br>${step.detail}</div>`).join("<hr>");
        document.getElementById("agentFindings").innerHTML = (run.findings || []).map((item) => `- ${item}`).join("<br>");
        document.getElementById("agentRecommendations").innerHTML = (run.recommendations || []).map((item) => `<div><strong>${item.campaign_name}</strong><br>${item.reason}<br>${item.suggested_action}</div>`).join("<hr>");
        document.getElementById("agentPrompt").textContent = run.prompt || "";
        document.getElementById("agentLlmOutput").textContent = run.llm_output || "";
        document.getElementById("agentNextActions").innerHTML = (run.next_actions || []).map((item) => `- ${item}`).join("<br>");
    }

    getWorkflowStatusLabel(status) {
        const normalized = String(status || "").toLowerCase();
        if (["done", "completed", "success"].includes(normalized)) return this.t("workflowStatusDone");
        if (["running", "in_progress"].includes(normalized)) return this.t("workflowStatusRunning");
        return this.t("workflowStatusPending");
    }
}

const agentUI = new AgentUI();
