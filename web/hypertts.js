// build using:
// npm run build

import HyperTTS, {configureEditorHyperTTS} from "./HyperTTS.svelte";

$editorToolbar.then((editorToolbar) => {
    console.log(configureEditorHyperTTS);
    editorToolbar.toolbar.insertGroup({component: HyperTTS, id: "hypertts"});
});
