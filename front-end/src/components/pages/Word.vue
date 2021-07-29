<template>
    <md-content class="md-elevation-3 word">
        <div class="md-layout">
            <div class="md-layout-item md-size-20">
                <div class="reading" v-if="word.vi_text != null">{{word.vi_text}}</div>
                <div class="kanji" v-if="word.kanji_text != null">{{word.kanji_text}}</div>
                <div class="hiragana" v-if="word.hiragana_text != null">{{word.hiragana_text}}</div>
                <div class="katakana" v-if="word.katakana_text != null">{{word.katakana_text}}</div>
                <div class="note" v-if="word.example != null">{{word.example}}</div>
                <div class="note" v-if="word.description != null">{{word.description}}</div>
            </div>

            <div class="md-layout-item md-size-60">
                <div>
                    <div class="chips">
                        <md-chip class="md-primary">
                            {{word.vi_text}}
                        </md-chip>
                        <md-chip class="md-primary">
                            {{word.kanji_text}}
                        </md-chip>
                    </div>

                    <div>
                        {{i + 1}}. {{word.vi_text.join('; ')}}
                    </div>
                    <div>
                        {{i + 1}}. {{word.kanji_text.join('; ')}}
                    </div>
                </div>
            </div>

            <div class="md-layout-item md-size-5">
                <Bookmark :type="0" :id="word.id"/>
            </div>
        </div>
    </md-content>
</template>

<style scoped lang="scss">
    @import '../../../node_modules/vue-material/dist/theme/engine';

    .md-layout {
        margin: 15px 30px;

        @media screen and (max-width: 768px) {
            div {
                padding: 0 !important;
                text-align: center;
                min-width: 100%;
                max-width: 100%;
            }
        }

        .buttons .md-button {
            margin-left: 0;
            background-color: rgba(white, 0.1);
            z-index: 1;
        }

        .md-layout-item {
            padding: 20px 0;
        }

        .md-chip {
            margin: 10px 3px;
        }

        .note {
            color: md-get-palette-color(gray, 500);
            font-size: 14px;
        }

        .reading {
            color: md-get-palette-color(gray, 500);
            font-size: 16px;
        }

        .kanji {
            font-size: 36px;
            line-height: normal;
        }

        .hiragana, .katakana {
            font-size: 20px;
            line-height: normal;
        }

    }
</style>

<script>
    import Bookmark from "../Bookmark";
    export default {
        name: "Word",
        components: {Bookmark},
        props: {
            word: Object
        }
    }
</script>
