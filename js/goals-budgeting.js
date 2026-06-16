// Goals & Budgeting JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Sample data for goals
    const goals = [
        {
            id: 1,
            name: 'Emergency Fund',
            target: 15000,
            current: 8500,
            deadline: '2024-12-31',
            category: 'Savings',
            status: 'active'
        },
        {
            id: 2,
            name: 'Vacation to Europe',
            target: 5000,
            current: 3200,
            deadline: '2024-08-15',
            category: 'Travel',
            status: 'active'
        },
        {
            id: 3,
            name: 'New Car Down Payment',
            target: 8000,
            current: 8000,
            deadline: '2024-06-01',
            category: 'Purchase',
            status: 'completed'
        },
        {
            id: 4,
            name: 'Home Renovation',
            target: 25000,
            current: 12500,
            deadline: '2025-03-31',
            category: 'Home',
            status: 'active'
        },
        {
            id: 5,
            name: 'Retirement Fund',
            target: 100000,
            current: 45000,
            deadline: '2040-12-31',
            category: 'Investment',
            status: 'active'
        }
    ];

    // Sample data for budget categories
    const budgetCategories = [
        {
            name: 'Housing',
            budgeted: 2500,
            spent: 2100,
            color: '#3B82F6'
        },
        {
            name: 'Food & Dining',
            budgeted: 800,
            spent: 650,
            color: '#10B981'
        },
        {
            name: 'Transportation',
            budgeted: 400,
            spent: 380,
            color: '#F59E0B'
        },
        {
            name: 'Entertainment',
            budgeted: 300,
            spent: 450,
            color: '#EF4444'
        },
        {
            name: 'Utilities',
            budgeted: 200,
            spent: 180,
            color: '#8B5CF6'
        },
        {
            name: 'Healthcare',
            budgeted: 150,
            spent: 120,
            color: '#06B6D4'
        }
    ];

    // Initialize the page
    initializeGoals();
    initializeBudgetCategories();
    initializeChart();
    setupEventListeners();

    function initializeGoals() {
        const goalsList = document.getElementById('goalsList');
        const activeGoalsCount = document.getElementById('activeGoalsCount');

        // Count active goals
        const activeCount = goals.filter(goal => goal.status === 'active').length;
        activeGoalsCount.textContent = activeCount;

        // Render goals
        goalsList.innerHTML = goals.map(goal => {
            const progress = (goal.current / goal.target) * 100;
            const isCompleted = goal.status === 'completed';
            const progressColor = isCompleted ? 'bg-green-500' : 'bg-blue-500';

            return `
                <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div class="flex items-center space-x-4">
                        <div class="w-12 h-12 ${isCompleted ? 'bg-green-100' : 'bg-blue-100'} rounded-xl flex items-center justify-center">
                            <i class="fas fa-${isCompleted ? 'check' : 'bullseye'} ${isCompleted ? 'text-green-600' : 'text-blue-600'}"></i>
                        </div>
                        <div>
                            <h4 class="font-semibold">${goal.name}</h4>
                            <p class="text-sm text-gray-500">${goal.category} • Due ${formatDate(goal.deadline)}</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-4">
                        <div class="text-right">
                            <div class="font-bold">$${goal.current.toLocaleString()}</div>
                            <div class="text-sm text-gray-500">of $${goal.target.toLocaleString()}</div>
                        </div>
                        <div class="w-24">
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="${progressColor} h-2 rounded-full" style="width: ${Math.min(progress, 100)}%"></div>
                            </div>
                            <div class="text-xs text-center mt-1">${Math.round(progress)}%</div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    function initializeBudgetCategories() {
        const budgetCategoriesContainer = document.getElementById('budgetCategories');

        budgetCategoriesContainer.innerHTML = budgetCategories.map(category => {
            const spentPercentage = (category.spent / category.budgeted) * 100;
            const isOverBudget = category.spent > category.budgeted;

            return `
                <div class="p-4 bg-gray-50 rounded-xl">
                    <div class="flex justify-between items-center mb-2">
                        <h4 class="font-semibold">${category.name}</h4>
                        <span class="text-sm ${isOverBudget ? 'text-red-600' : 'text-gray-600'}">
                            $${category.spent} / $${category.budgeted}
                        </span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="h-2 rounded-full" style="width: ${Math.min(spentPercentage, 100)}%; background-color: ${category.color}"></div>
                    </div>
                    <div class="flex justify-between items-center mt-2">
                        <span class="text-xs text-gray-500">${Math.round(spentPercentage)}% used</span>
                        ${isOverBudget ? '<span class="text-xs text-red-600 font-medium">Over budget</span>' : ''}
                    </div>
                </div>
            `;
        }).join('');
    }

    function initializeChart() {
        const ctx = document.getElementById('budgetChart').getContext('2d');

        const data = {
            labels: budgetCategories.map(cat => cat.name),
            datasets: [
                {
                    label: 'Budgeted',
                    data: budgetCategories.map(cat => cat.budgeted),
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Spent',
                    data: budgetCategories.map(cat => cat.spent),
                    backgroundColor: 'rgba(239, 68, 68, 0.5)',
                    borderColor: 'rgba(239, 68, 68, 1)',
                    borderWidth: 1
                }
            ]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        };

        new Chart(ctx, config);
    }

    function setupEventListeners() {
        const addGoalBtn = document.getElementById('addGoalBtn');
        const addGoalModal = document.getElementById('addGoalModal');
        const closeModal = document.getElementById('closeModal');
        const cancelBtn = document.getElementById('cancelBtn');
        const goalForm = document.getElementById('goalForm');

        addGoalBtn.addEventListener('click', () => {
            addGoalModal.classList.remove('hidden');
        });

        closeModal.addEventListener('click', () => {
            addGoalModal.classList.add('hidden');
        });

        cancelBtn.addEventListener('click', () => {
            addGoalModal.classList.add('hidden');
        });

        goalForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // In a real app, this would send data to a server
            alert('Goal created successfully!');
            addGoalModal.classList.add('hidden');
            goalForm.reset();
        });

        // Close modal when clicking outside
        addGoalModal.addEventListener('click', (e) => {
            if (e.target === addGoalModal) {
                addGoalModal.classList.add('hidden');
            }
        });
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
});