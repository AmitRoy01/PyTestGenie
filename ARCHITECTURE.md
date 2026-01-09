# PyTestGenie - Architecture Documentation

## Overview
PyTestGenie is a unified platform combining automated test generation and test smell detection for Python projects.

## Architecture

### Backend (Flask API)
```
backend/
├── app_unified.py              # Main Flask application
├── config/
│   └── settings.py            # Configuration management
├── routes/
│   ├── test_generation.py     # /api/test-generator endpoints
│   └── smell_detection.py     # /api/smell-detector endpoints
├── modules/
│   ├── test_generator/        # Test generation logic
│   └── smell_detector/        # Smell detection logic
```

### Frontend (React)
```
frontend/src/
├── App.jsx                    # Main application with tab navigation
├── components/
│   ├── TestGenerator.jsx     # Test generation UI
│   └── SmellDetector.jsx     # Smell detection UI
```

## Module Responsibilities

### Test Generator Module
- **pynguin_generator.py**: Interfaces with Pynguin for automatic test generation
- **ai_generator.py**: Uses OpenAI API (via HuggingFace) for AI-powered test generation
- **models.py**: Data models for test generation results

### Smell Detector Module
- **analyzer.py**: Main coordinator for smell detection
- **detector.py**: Smell detection algorithms
- **python_parser.py**: Parses Python test files
- **report_generator.py**: Generates HTML reports

## API Endpoints

### Test Generation
- `POST /api/test-generator/generate-tests/pynguin` - Generate using Pynguin
- `GET /api/test-generator/generate-tests/stream/<task_id>` - Stream Pynguin logs
- `POST /api/test-generator/generate-tests/ai` - Generate using AI

### Smell Detection
- `POST /api/smell-detector/analyze/code` - Analyze code string
- `POST /api/smell-detector/analyze/file` - Analyze uploaded file
- `POST /api/smell-detector/analyze/directory` - Analyze multiple files
- `POST /api/smell-detector/analyze/github` - Analyze GitHub repo
- `GET /api/smell-detector/report` - Get HTML report

## Data Flow

### Test Generation Flow
1. User enters code in frontend
2. Frontend sends POST to backend API
3. Backend invokes appropriate generator (Pynguin/AI)
4. Results streamed (Pynguin) or returned directly (AI)
5. Frontend displays generated tests
6. User can trigger smell detection on generated tests

### Smell Detection Flow
1. User provides code/file/directory/GitHub URL
2. Frontend sends to backend API
3. Backend:
   - Saves/clones files if needed
   - Runs analyzer on test files
   - Generates HTML report
4. Frontend displays results summary
5. User can view detailed HTML report

## File Responsibilities

### Backend Files

**app_unified.py**
- Application factory
- Blueprint registration
- CORS configuration
- Root endpoints

**config/settings.py**
- Environment configuration
- Flask settings
- API tokens

**routes/test_generation.py**
- Test generation endpoints
- Task queue management for Pynguin
- SSE streaming for logs

**routes/smell_detection.py**
- Smell detection endpoints
- File upload handling
- GitHub integration
- Report serving

**modules/test_generator/pynguin_generator.py**
- Pynguin command execution
- Log streaming
- Async task management

**modules/test_generator/ai_generator.py**
- OpenAI API integration
- Prompt engineering
- Response parsing

**modules/smell_detector/analyzer.py**
- File analysis coordination
- Report generation
- Test file detection

### Frontend Files

**App.jsx**
- Tab navigation (Generator/Detector)
- Component routing
- Application layout

**components/TestGenerator.jsx**
- Method selection (Pynguin/AI)
- Code input
- Generation triggering
- Result display
- Smell detection integration

**components/SmellDetector.jsx**
- Mode selection (Code/File/Directory/GitHub)
- Input handling
- Analysis triggering
- Result display

## Configuration

### Environment Variables
- `HF_TOKEN`: HuggingFace API token for AI generation
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: Environment (development/production)
- `CORS_ORIGINS`: Allowed CORS origins

### Settings Classes
- `Config`: Base configuration
- `DevelopmentConfig`: Development settings
- `ProductionConfig`: Production settings

## Error Handling

### Backend
- Try-catch blocks in all endpoints
- Meaningful error messages
- HTTP status codes
- Error logging

### Frontend
- axios error handling
- User-friendly alerts
- Loading states
- Validation

## Security Considerations

1. **File Uploads**: Secure filename sanitization
2. **CORS**: Configured origins only
3. **API Tokens**: Environment variables only
4. **Temporary Files**: Cleaned up after use
5. **Input Validation**: All inputs validated

## Performance Optimizations

1. **Streaming**: SSE for Pynguin logs
2. **Async**: Background tasks for long operations
3. **Cleanup**: Temporary files removed immediately
4. **Caching**: Static files cached

## Deployment Notes

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
python app_unified.py
```

### Frontend Deployment
```bash
cd frontend
npm install
npm run build
npm run preview
```

### Production Considerations
- Use production WSGI server (gunicorn/uwsgi)
- Set FLASK_ENV=production
- Configure proper CORS origins
- Use environment-specific .env files
- Enable HTTPS
- Set up proper logging

## Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## Maintenance

### Adding New Features
1. Create module in `backend/modules/`
2. Create routes in `backend/routes/`
3. Register blueprint in `app_unified.py`
4. Create React component in `frontend/src/components/`
5. Update App.jsx navigation

### Updating Dependencies
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

## Troubleshooting Guide

### Common Issues

**Backend won't start**
- Check .env file exists
- Verify Python dependencies installed
- Check port 5000 availability

**Frontend won't start**
- Run `npm install`
- Check Node.js version >= 14
- Verify port 3000 availability

**CORS errors**
- Check CORS_ORIGINS in .env
- Verify backend is running
- Check API_BASE URLs in frontend

**Generation fails**
- Verify HF_TOKEN in .env
- Check code is valid Python
- Review backend logs

## Future Enhancements

1. User authentication
2. Test history/storage
3. Custom smell detection rules
4. Batch processing
5. Export to different formats
6. Integration with CI/CD
7. Performance metrics
8. Test coverage analysis
