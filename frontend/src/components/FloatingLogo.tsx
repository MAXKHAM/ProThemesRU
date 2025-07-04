import React from 'react';
import { motion } from 'framer-motion';

const FloatingLogo: React.FC = () => {
  return (
    <motion.div
      className="fixed top-4 left-4 z-50 cursor-pointer"
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
    >
      <motion.div
        animate={{
          y: [0, -10, 0],
          x: [-5, 5, -5],
          rotate: [0, 5, 0],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="w-12 h-12 rounded-full bg-primary-600 flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300"
      >
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V10.125m0 0h3.375m0 0h3.375m0 0V1.25m-6.75 15.625h3.375m0 0h3.375m0 0V5.625m0 0h3.375m0 0v11.25m-10.125-11.25h3.375m0 0h3.375m0 0V4.6875m0 0h3.375m0 0v12.1875m-6.75-10.9375L12 19.125l1.5-1.5m-4.5-6.25h.008v.008H12v-.008h.008m0 0h.008v.008H12m-4.5 0h3.375m0 0h3.375m0 0V4.6875m0 0h3.375m0 0v10.125m-3.375 0h3.375" />
        </svg>
      </motion.div>
    </motion.div>
  );
};

export default FloatingLogo;
