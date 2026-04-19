import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helper?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helper,
  className = '',
  id,
  ...props
}) => {
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
  
  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-gray-700 mb-1.5">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`
          w-full px-3 py-2 rounded-lg border transition-colors duration-200
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
          ${error 
            ? 'border-red-500 focus:ring-red-500' 
            : 'border-gray-300 hover:border-gray-400'
          }
          ${className}
        `}
        {...props}
      />
      {error && <p className="mt-1.5 text-sm text-red-600">{error}</p>}
      {helper && !error && <p className="mt-1.5 text-sm text-gray-500">{helper}</p>}
    </div>
  );
};