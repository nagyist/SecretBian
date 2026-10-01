// Run with: osascript -l JavaScript set-macos-file-icon.js ICON FILE
ObjC.import('AppKit');

function run(args) {
    if (args.length !== 2) {
        throw new Error('Expected icon path and executable path');
    }
    const image = $.NSImage.alloc.initWithContentsOfFile($(args[0]));
    if (!image || !image.isValid) {
        throw new Error('Cannot load icon: ' + args[0]);
    }
    if (!$.NSWorkspace.sharedWorkspace.setIconForFileOptions(image, $(args[1]), 0)) {
        throw new Error('Cannot set Finder icon: ' + args[1]);
    }
}
