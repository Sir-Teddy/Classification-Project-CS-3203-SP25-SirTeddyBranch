const express = require('express');
const jwt = require('jsonwebtoken');
const LessonPlan = require('../models/LessonPlan');
const router = express.Router();

// Middleware to check if user is authenticated
const authenticate = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

// Submit a lesson plan
router.post('/', authenticate, async (req, res) => {
  const { title, content } = req.body;
  const teacher = req.user.id;

  try {
    const newLessonPlan = new LessonPlan({ title, content, teacher });
    await newLessonPlan.save();
    res.status(201).json({ message: 'Lesson plan submitted successfully!' });
  } catch (err) {
    res.status(500).json({ error: 'Error submitting lesson plan' });
  }
});

// Get all lesson plans (for administrators)
router.get('/', authenticate, async (req, res) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Access denied' });
  }

  try {
    const lessonPlans = await LessonPlan.find().populate('teacher', 'email');
    res.json(lessonPlans);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching lesson plans' });
  }
});

// Approve or reject a lesson plan (for administrators)
router.patch('/:id', authenticate, async (req, res) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Access denied' });
  }

  const { status } = req.body;

  try {
    const lessonPlan = await LessonPlan.findById(req.params.id);
    if (!lessonPlan) {
      return res.status(404).json({ error: 'Lesson plan not found' });
    }

    lessonPlan.status = status;
    await lessonPlan.save();
    res.json({ message: 'Lesson plan updated successfully!' });
  } catch (err) {
    res.status(500).json({ error: 'Error updating lesson plan' });
  }
});

module.exports = router;