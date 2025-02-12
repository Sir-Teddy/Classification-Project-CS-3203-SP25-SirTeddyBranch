const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const authRoutes = require('./routes/auth');
const lessonPlanRoutes = require('./routes/lessonPlans');

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());

// MongoDB Connection
require('dotenv').config();
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.error('MongoDB Connection Error:', err));

app.get('/', (req, res) => res.send('API is running...'));

const PORT = process.env.PORT || 8080;

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/lessonPlans', lessonPlanRoutes);

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
