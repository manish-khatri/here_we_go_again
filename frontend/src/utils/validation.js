// Form validation utilities

export const validators = {
  required: (value) => {
    if (!value || value.toString().trim() === '') {
      return 'This field is required'
    }
    return null
  },

  email: (value) => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    if (value && !emailPattern.test(value)) {
      return 'Please enter a valid email address'
    }
    return null
  },

  minLength: (min) => (value) => {
    if (value && value.length < min) {
      return `Must be at least ${min} characters long`
    }
    return null
  },

  maxLength: (max) => (value) => {
    if (value && value.length > max) {
      return `Must be no more than ${max} characters long`
    }
    return null
  },

  password: (value) => {
    if (value && value.length < 8) {
      return 'Password must be at least 8 characters long'
    }
    if (value && !/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
      return 'Password must contain at least one uppercase letter, one lowercase letter, and one number'
    }
    return null
  },

  date: (value) => {
    if (value) {
      const date = new Date(value)
      if (isNaN(date.getTime())) {
        return 'Please enter a valid date'
      }
      // Check if date is in the future for quiz dates
      if (date < new Date()) {
        return 'Quiz date must be in the future'
      }
    }
    return null
  },

  time: (value) => {
    if (value) {
      const timePattern = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/
      if (!timePattern.test(value)) {
        return 'Please enter a valid time (HH:MM)'
      }
    }
    return null
  },

  number: (value) => {
    if (value && isNaN(Number(value))) {
      return 'Please enter a valid number'
    }
    return null
  },

  range: (min, max) => (value) => {
    const num = Number(value)
    if (value && (num < min || num > max)) {
      return `Value must be between ${min} and ${max}`
    }
    return null
  }
}

export const validateField = (value, validations) => {
  for (const validation of validations) {
    const error = validation(value)
    if (error) {
      return error
    }
  }
  return null
}

export const validateForm = (formData, validationRules) => {
  const errors = {}
  let isValid = true

  for (const [field, validations] of Object.entries(validationRules)) {
    const error = validateField(formData[field], validations)
    if (error) {
      errors[field] = error
      isValid = false
    }
  }

  return { isValid, errors }
}

export const addBootstrapValidation = (element, isValid, errorMessage) => {
  // Remove existing validation classes
  element.classList.remove('is-valid', 'is-invalid')
  
  // Remove existing feedback
  const existingFeedback = element.parentNode.querySelector('.invalid-feedback, .valid-feedback')
  if (existingFeedback) {
    existingFeedback.remove()
  }

  if (isValid) {
    element.classList.add('is-valid')
  } else {
    element.classList.add('is-invalid')
    
    // Add error message
    if (errorMessage) {
      const feedback = document.createElement('div')
      feedback.className = 'invalid-feedback'
      feedback.textContent = errorMessage
      element.parentNode.appendChild(feedback)
    }
  }
}

export const validateEmailUniqueness = async (email) => {
  try {
    const response = await fetch('/api/validate/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    })
    
    const result = await response.json()
    return result.valid ? null : result.error
  } catch (error) {
    return 'Unable to validate email'
  }
}
