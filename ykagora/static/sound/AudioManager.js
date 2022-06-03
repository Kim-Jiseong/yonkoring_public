var timer, sound, id;
var currentMuteState = false;
function callPlacedSound() {
    stopAllSound();
    sound = new Howl({
        src: [sound_url + 'placeCall.mp3']
    });
    id = sound.play();
}

function incomingCallSound() {
    stopAllSound();
    sound = new Howl({
        src: [sound_url + 'incomingCall.mp3']
    });
    id = sound.play();
}

function endCallSound() {
    sound = new Howl({
        src: [sound_url + 'endCall.mp3']
    });
    id = sound.play();
}

function ringingToneSound() {
    sound = new Howl({
        src: [sound_url + 'ringingTone.mp3'],
        loop: true,
    });
    id = sound.play();
}

function stopAllSound() {
    sound.stop();
}

function muteSound() {
    sound.mute(true, id);
    currentMuteState = true;
    
}

function unmuteSound() {
    sound.mute(false, id);
    currentMuteState = false;
}

function getMuteState() {
    return currentMuteState;
}
