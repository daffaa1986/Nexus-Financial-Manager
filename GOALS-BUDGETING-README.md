# Goals & Budgeting Page

Halaman Goals & Budgeting adalah bagian dari sistem manajemen keuangan Nexus Finance yang memungkinkan pengguna untuk:

## Fitur Utama

### 1. Financial Goals Management
- **Menambah Goal Baru**: Form modal untuk membuat goal keuangan baru
- **Tracking Progress**: Visual progress bar untuk setiap goal
- **Kategori Goals**: Savings, Investment, Debt Payment, Major Purchase
- **Status Tracking**: Active, Completed goals

### 2. Budget Categories
- **Kategori Pengeluaran**: Housing, Food, Transportation, Entertainment, dll.
- **Budget vs Actual**: Perbandingan antara budget yang ditetapkan vs pengeluaran aktual
- **Visual Indicators**: Progress bars dengan warna-warni
- **Over Budget Alerts**: Notifikasi ketika pengeluaran melebihi budget

### 3. Analytics & Charts
- **Budget vs Actual Chart**: Chart batang untuk membandingkan budget dan pengeluaran
- **Savings Rate Tracking**: Persentase tabungan bulanan
- **Goal Achievement Metrics**: Statistik pencapaian goals

## File Structure

```
Goals-Budgeting.html      # Main HTML page
js/goals-budgeting.js     # JavaScript functionality
css/style.css            # Custom styles (updated)
assets/goals-icons.svg   # Custom SVG icons
```

## Technologies Used

- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts and graphs
- **Font Awesome**: Icons
- **Vanilla JavaScript**: DOM manipulation and interactivity

## Key Components

### Goals Overview Cards
Menampilkan statistik utama:
- Active Goals Count
- Total Monthly Budget
- Current Savings Rate

### Goals List
Daftar semua financial goals dengan:
- Progress visualization
- Target amounts
- Deadlines
- Categories

### Budget Categories Grid
Grid responsif menampilkan:
- Budget allocations
- Actual spending
- Progress indicators
- Over-budget warnings

### Interactive Chart
Chart.js implementation untuk:
- Budget vs spending comparison
- Monthly tracking
- Category breakdown

## Modal Forms

### Add New Goal Modal
Form untuk membuat goal baru dengan fields:
- Goal Name
- Target Amount
- Target Date
- Category selection

## Responsive Design

Halaman dirancang responsive dengan:
- Mobile-first approach
- Flexible grid layouts
- Adaptive chart sizing
- Touch-friendly interactions

## Data Structure

### Goals Object
```javascript
{
    id: number,
    name: string,
    target: number,
    current: number,
    deadline: string,
    category: string,
    status: 'active' | 'completed'
}
```

### Budget Categories Object
```javascript
{
    name: string,
    budgeted: number,
    spent: number,
    color: string
}
```

## Future Enhancements

- Real-time data synchronization
- Goal sharing features
- Advanced budgeting algorithms
- Integration with banking APIs
- Goal achievement notifications
- Historical trend analysis