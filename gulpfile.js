const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require('gulp-autoprefixer');
const cleanCSS = require('gulp-clean-css');
const rename = require('gulp-rename');

// Пути
const paths = {
  scss: {
    src: 'static/scss/**/*.scss',
    dest: 'static/css'
  }
};

// Компиляция SCSS
function compileScss() {
  return gulp.src(paths.scss.src)
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({
      cascade: false
    }))
    .pipe(cleanCSS())
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest(paths.scss.dest));
}

// Следим за изменениями
function watchFiles() {
  gulp.watch(paths.scss.src, compileScss);
}

// Экспортируем задачи
exports.default = gulp.series(compileScss, watchFiles);
exports.compileScss = compileScss;
