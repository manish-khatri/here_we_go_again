# Quiz Master Design System

## Overview
The Quiz Master application has been redesigned with a clean, modern interface using a pastel blue color theme. The design emphasizes simplicity, clarity, and excellent user experience.

## Color Palette

### Primary Colors
- **Primary Blue**: `#7FB3D3` - Main brand color for buttons, links, and highlights
- **Light Blue**: `#B8D4E3` - Secondary color for borders and subtle elements
- **Lighter Blue**: `#E8F4F8` - Background color for cards and hover states
- **Dark Blue**: `#5A8BA8` - Hover state for primary elements
- **Accent Blue**: `#A8D5E8` - Additional accent color

### Neutral Colors
- **Text Dark**: `#2C3E50` - Primary text color
- **Text Light**: `#6C757D` - Secondary text color
- **White**: `#FFFFFF` - Background color
- **Gray 100**: `#F8F9FA` - Light background
- **Gray 200**: `#E9ECEF` - Border color
- **Gray 300**: `#DEE2E6` - Input borders

### Semantic Colors
- **Success**: `#28A745` - Success states and completed items
- **Warning**: `#FFC107` - Warning states and timers
- **Danger**: `#DC3545` - Error states and destructive actions
- **Info**: `#17A2B8` - Information states

## Typography
- **Font Family**: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- **Line Height**: 1.6 for optimal readability
- **Font Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

## Components

### Buttons
- **Primary**: Pastel blue background with white text
- **Secondary**: Light gray background with dark text
- **Success**: Green background for positive actions
- **Danger**: Red background for destructive actions
- **Border Radius**: 8px for modern appearance
- **Hover Effects**: Subtle transform and shadow effects

### Cards
- **Background**: White with subtle shadow
- **Border Radius**: 12px for modern appearance
- **Header**: Light blue background with dark text
- **Hover Effects**: Enhanced shadow and subtle transform

### Forms
- **Input Fields**: 2px border with 8px border radius
- **Focus State**: Blue border with subtle shadow
- **Validation**: Red border for invalid states

### Tables
- **Header**: Light blue background with dark text
- **Rows**: White background with subtle hover effect
- **Borders**: Light gray borders for separation

### Navigation
- **Background**: White with subtle shadow
- **Links**: Dark text with blue hover state
- **Active State**: Light blue background

## Layout Principles

### Spacing
- **Container Padding**: 2rem for main content areas
- **Component Spacing**: 1rem for standard spacing
- **Card Padding**: 1.5rem for comfortable content

### Grid System
- Uses Bootstrap 5 grid system
- Responsive breakpoints for mobile-first design
- Consistent column layouts across views

### Responsive Design
- **Mobile**: Single column layouts with stacked elements
- **Tablet**: Two-column layouts where appropriate
- **Desktop**: Multi-column layouts with sidebars

## Animation & Interactions

### Transitions
- **Duration**: 0.2s for quick, responsive feel
- **Easing**: Ease-in-out for smooth animations
- **Hover Effects**: Subtle transforms and color changes

### Loading States
- **Spinners**: Blue color matching primary theme
- **Skeleton Loading**: Light gray placeholders
- **Progress Indicators**: Blue progress bars

## Accessibility

### Color Contrast
- All text meets WCAG AA contrast requirements
- High contrast for important information
- Color is not the only indicator of state

### Focus States
- Clear focus indicators for keyboard navigation
- Consistent focus styling across components
- Visible focus rings for all interactive elements

### Screen Reader Support
- Semantic HTML structure
- Proper ARIA labels and roles
- Descriptive alt text for images

## Implementation

### CSS Variables
The design system uses CSS custom properties for consistent theming:

```css
:root {
  --primary-blue: #7FB3D3;
  --light-blue: #B8D4E3;
  --lighter-blue: #E8F4F8;
  --dark-blue: #5A8BA8;
  --accent-blue: #A8D5E8;
  --text-dark: #2C3E50;
  --text-light: #6C757D;
  --white: #FFFFFF;
  --gray-100: #F8F9FA;
  --gray-200: #E9ECEF;
  --gray-300: #DEE2E6;
  --success: #28A745;
  --warning: #FFC107;
  --danger: #DC3545;
  --info: #17A2B8;
}
```

### Bootstrap Integration
- Leverages Bootstrap 5 components and utilities
- Custom CSS overrides for brand colors
- Consistent spacing and typography scales
- Responsive grid system

## Best Practices

### Consistency
- Use the same color variables throughout
- Maintain consistent spacing patterns
- Follow established component patterns

### Performance
- Minimal CSS with efficient selectors
- Optimized animations and transitions
- Responsive images and assets

### Maintainability
- Well-organized CSS structure
- Clear naming conventions
- Documented component usage

## Future Enhancements
- Dark mode support
- Additional color themes
- Enhanced animation library
- Advanced component variations 