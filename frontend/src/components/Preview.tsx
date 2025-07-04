import React from 'react';
import { useEditor } from '../contexts/EditorContext';
import { useTheme } from '@mui/material';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

interface BlockProps {
  type: string;
  content: any;
  style: any;
}

const BlockPreview: React.FC<BlockProps> = ({ type, content, style }) => {
  const theme = useTheme();
  const { ref, inView } = useInView({ threshold: 0.1 });

  const renderBlock = () => {
    switch (type) {
      case 'text':
        return (
          <Typography
            variant="body1"
            sx={{
              ...style,
              color: theme.palette.text.primary,
              transition: 'all 0.3s ease',
            }}
          >
            {content}
          </Typography>
        );
      case 'image':
        return (
          <Box
            sx={{
              ...style,
              borderRadius: '12px',
              overflow: 'hidden',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              background: `url(${content.src})`,
            }}
          />
        );
      case 'button':
        return (
          <Button
            variant="contained"
            sx={{
              ...style,
              backgroundColor: theme.palette.secondary.main,
              '&:hover': {
                backgroundColor: theme.palette.secondary.dark,
              },
            }}
          >
            {content.text}
          </Button>
        );
      // Добавьте другие типы блоков по аналогии
      default:
        return null;
    }
  };

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ duration: 0.6 }}
    >
      {renderBlock()}
    </motion.div>
  );
};

const Preview: React.FC = () => {
  const { blocks, previewMode } = useEditor();
  const theme = useTheme();

  return (
    <Box
      sx={{
        width: '100%',
        height: '100vh',
        background: theme.palette.background.paper,
        overflow: 'auto',
        position: 'relative',
        p: 4,
      }}
    >
      <Box
        sx={{
          width: '100%',
          maxWidth: '1200px',
          mx: 'auto',
          position: 'relative',
        }}
      >
        {blocks.map((block) => (
          <BlockPreview
            key={block.id}
            type={block.type}
            content={block.content}
            style={block.style}
          />
        ))}
      </Box>
    </Box>
  );
};

export default Preview;
