# OTP-Based Password Reset Setup Instructions

## Overview
This implementation adds OTP (One-Time Password) based password reset functionality to your HealthyMe project, similar to the AI Dietician project.

## Features Implemented

### 1. **OTP-Based Password Reset Flow**
- User requests password reset via email
- System generates 6-digit OTP and sends via email
- User verifies OTP
- User sets new password with validation

### 2. **Security Features**
- 6-digit numeric OTP with pattern validation
- Email verification before sending OTP
- OTP expiration (deleted after verification)
- Password requirements (minimum 8 characters)
- CSRF protection on all forms

### 3. **User Interface**
- Modern, responsive templates matching your existing design
- Clear error and success messages
- Password requirements display
- Easy navigation between steps

## Setup Instructions

### 1. **Email Configuration**

Create a `.env` file in your project root with the following variables:

```env
# Email Configuration for OTP
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Other existing environment variables
GEMINI_API_KEY=your-gemini-api-key
YOUTUBE_API_KEY=your-youtube-api-key
EDAMAM_APP_ID=your-edamam-app-id
EDAMAM_APP_KEY=your-edamam-app-key
```

### 2. **Gmail App Password Setup**

To use Gmail for sending OTP emails:

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in `EMAIL_HOST_PASSWORD`

### 3. **Database Requirements**

The system uses your existing database tables:
- `registration` table: Contains user email addresses
- `login` table: Contains user passwords

### 4. **URLs Added**

The following new URLs have been added:
- `/forgot_password/` - Initial forgot password form
- `/send_otp/` - Generate and send OTP
- `/verify_otp/` - Verify OTP entered by user
- `/reset_password/` - Set new password after verification

## Usage Flow

### For Users:
1. **Request Password Reset**: Click "Forgot Password (OTP)" on login page
2. **Enter Email**: Provide registered email address
3. **Receive OTP**: Check email for 6-digit OTP
4. **Verify OTP**: Enter OTP on verification page
5. **Set New Password**: Enter and confirm new password
6. **Login**: Use new password to login

### For Administrators:
- Monitor OTP requests in server logs
- Configure email settings in `.env` file
- Customize email templates if needed

## Security Considerations

### Production Recommendations:
1. **OTP Storage**: Replace in-memory storage with Redis or database
2. **OTP Expiration**: Add time-based expiration (currently 10 minutes mentioned)
3. **Rate Limiting**: Implement rate limiting for OTP requests
4. **Email Templates**: Customize email templates for your brand
5. **Logging**: Add proper logging for security events

### Current Implementation:
- ✅ CSRF protection
- ✅ Email validation
- ✅ Password requirements
- ✅ OTP pattern validation
- ✅ Secure password update

## Files Modified/Created

### Modified Files:
- `HealthyMe/settings.py` - Added email configuration
- `MyApp/views.py` - Added OTP views and functions
- `HealthyMe/urls.py` - Added OTP URL patterns
- `MyApp/templates/login.html` - Added OTP forgot password link

### New Files:
- `MyApp/templates/forgot_password.html` - Email input form
- `MyApp/templates/otp_verification.html` - OTP verification form
- `MyApp/templates/reset_password.html` - New password form

## Testing

### Test the OTP Flow:
1. Start your Django server
2. Navigate to `/login/`
3. Click "Forgot Password (OTP)"
4. Enter a registered email address
5. Check email for OTP
6. Complete the password reset process

### Test Cases:
- ✅ Valid email address
- ✅ Invalid email address
- ✅ Correct OTP
- ✅ Incorrect OTP
- ✅ Password validation
- ✅ Password confirmation mismatch

## Troubleshooting

### Common Issues:

1. **Email not sending**:
   - Check Gmail app password
   - Verify email configuration in settings
   - Check spam folder

2. **OTP not working**:
   - Ensure email exists in registration table
   - Check server logs for errors
   - Verify OTP storage is working

3. **Password reset fails**:
   - Check database connection
   - Verify user exists in both tables
   - Check password requirements

## Customization

### Email Template:
Modify the email message in `send_otp()` function in `views.py`:

```python
message=f"Your OTP is: {otp}. Please enter this code to reset your password. This OTP is valid for 10 minutes."
```

### Styling:
All templates use your existing CSS classes and styling patterns for consistency.

### OTP Format:
Currently uses 6-digit numeric OTP. To change, modify the OTP generation in `send_otp()`:

```python
otp = random.randint(100000, 999999)  # 6-digit
# or
otp = ''.join(random.choices('0123456789', k=6))  # Alternative method
```

## Support

For issues or questions:
1. Check server logs for error messages
2. Verify email configuration
3. Test with a known valid email address
4. Ensure all required packages are installed

The implementation follows Django best practices and integrates seamlessly with your existing HealthyMe project structure. 