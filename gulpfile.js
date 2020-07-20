const gulp = require("gulp");
const sass = require("gulp-sass");
sass.compiler = require("node-sass");
const autoprefixer = require('gulp-autoprefixer');
const imagemin = require('gulp-imagemin');
const iconfont = require('gulp-iconfont')
const consolidate = require('gulp-consolidate');
const async = require('async');
const runTimestamp = Math.round(Date.now()/1000);
const gih = require("gulp-include-html");


// SASS
gulp.task("sass", () => {
    return gulp
        .src("./src/scss/style.scss")
        .pipe(sass.sync())
        .pipe(gulp.dest("./centr_osvita/static/css"));
});

// Generate icon-font

gulp.task('iconfont', done => {
    const iconStream = gulp.src(['src/icons/*.svg']).pipe(
        iconfont({
            fontName: 'icons', // required
            formats: ['ttf', 'eot', 'woff', 'woff2'], // default, 'woff2' and 'svg' are available
            prependUnicode: false,
            normalize: true,
            fontHeight: 1000,
            timestamp: runTimestamp // recommended to get consistent builds when watching files
        })
    )

    return async.parallel(
        [
            cb => {
                iconStream.on('glyphs', glyphs => {
                    gulp
                        .src('src/scss/assets/_icons.scss')
                        .pipe(
                            consolidate('lodash', {
                                glyphs,
                                fontName: 'icons',
                                fontPath: '../fonts/',
                                className: 'icon',
                                formats: ['ttf', 'eot', 'woff', 'woff2', 'svg'] // default, 'woff2' and 'svg' are available
                            })
                        )
                        .pipe(gulp.dest('src/scss/'))
                        .on('finish', cb)
                })
            },
            cb => {
                iconStream.pipe(gulp.dest('public/fonts/')).on('finish', cb)
            }
        ],
        done
    )
})

//Watcher
gulp.task("watch", () => {
    gulp.watch("./src/scss/**/*.scss", gulp.series("sass"));
});


