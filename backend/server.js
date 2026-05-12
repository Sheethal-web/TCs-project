const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Mock Data
const kpiData = {
  liveRevenue: 15420,
  occupancyRate: 85,
  wasteRiskLevel: 'High'
};

const aiRecommendations = [
  {
    id: 1,
    trigger: 'Mutton Curry sales are 40% below target',
    action: 'Create a 15% discount bundle with Cold Coffee',
    impact: '+₹1,200 revenue',
    status: 'pending'
  },
  {
    id: 2,
    trigger: 'Tomatoes expiring in <12 hours',
    action: 'Recommend Tomato Soup as "Chef\'s Special" today',
    impact: 'Save ₹400 in waste',
    status: 'pending'
  }
];

const inventory = [
  { id: 1, name: 'Tomatoes', category: 'Groceries', status: 'Red', expiry: '< 12 hours', stock: '10 kg' },
  { id: 2, name: 'Milk', category: 'Beverages', status: 'Orange', expiry: '1 Day', stock: '20 Liters' },
  { id: 3, name: 'Chicken', category: 'Main Course', status: 'Green', expiry: '3 Days', stock: '50 kg' },
  { id: 4, name: 'Cold Coffee Beans', category: 'Beverages', status: 'Green', expiry: '1 Month', stock: '5 kg' },
  { id: 5, name: 'Mutton', category: 'Main Course', status: 'Orange', expiry: '2 Days', stock: '15 kg' },
];

const salesPrediction = [
  { time: '10:00', actual: 2000, predicted: 2200 },
  { time: '11:00', actual: 3500, predicted: 3000 },
  { time: '12:00', actual: 4000, predicted: 4500 },
  { time: '13:00', actual: 6000, predicted: 6500 }, // Peak
  { time: '14:00', actual: 5500, predicted: 5000 },
  { time: '15:00', actual: 3000, predicted: 3500 },
];

// API Routes
app.get('/api/kpi', (req, res) => res.json(kpiData));
app.get('/api/recommendations', (req, res) => res.json(aiRecommendations));
app.get('/api/inventory', (req, res) => res.json(inventory));
app.get('/api/sales', (req, res) => res.json(salesPrediction));

app.post('/api/recommendations/:id/approve', (req, res) => {
  const { id } = req.params;
  const index = aiRecommendations.findIndex(r => r.id === parseInt(id));
  if (index !== -1) {
    aiRecommendations[index].status = 'approved';
    res.json({ message: 'Recommendation approved successfully' });
  } else {
    res.status(404).json({ error: 'Recommendation not found' });
  }
});

app.post('/api/recommendations/:id/dismiss', (req, res) => {
  const { id } = req.params;
  const index = aiRecommendations.findIndex(r => r.id === parseInt(id));
  if (index !== -1) {
    aiRecommendations[index].status = 'dismissed';
    res.json({ message: 'Recommendation dismissed successfully' });
  } else {
    res.status(404).json({ error: 'Recommendation not found' });
  }
});

// IoT Endpoint: Receive camera data from Raspberry Pi
app.post('/api/cart/sync', (req, res) => {
  const { device_id, cart } = req.body;
  console.log(`\n[IoT CLOUD] Received camera data from ${device_id}:`, cart);

  // AWS Cloud ML Processing (Mocking the Python ML Service response)
  let offer = null;
  
  if (cart.includes('Laptop') && !cart.includes('Wireless Mouse')) {
    offer = { message: "30% OFF Wireless Mouse! (Essentials Bundle)" };
  } else if (cart.includes('DSLR Camera') && !cart.includes('SD Card')) {
    offer = { message: "50% OFF SD Card! (Ready-to-Shoot Kit)" };
  } else if (cart.includes('Pasta') && !cart.includes('Garlic Bread')) {
    offer = { message: "Free Garlic Bread! (Italian Classic)" };
  } else if (cart.includes('Diapers') && !cart.includes('Wet Wipes')) {
    offer = { message: "25% OFF Wet Wipes! (Hygiene Essential)" };
  }

  if (offer) {
    console.log(`[IoT CLOUD] AI Engine generated offer: ${offer.message}`);
  } else {
    console.log(`[IoT CLOUD] No bundle generated for this cart.`);
  }

  res.json({ success: true, offer });
});

app.listen(PORT, () => {
  console.log(`Smart AI Manager Backend running on port ${PORT}`);
});
