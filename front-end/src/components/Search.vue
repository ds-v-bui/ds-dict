<template>
    <div>
        <md-content class="bar">
            <label>
                <md-icon>search</md-icon>
                <md-field class="type">
                    <md-select @md-selected="search" id="type" name="type" v-model="settings.api.type">
                        <md-option value="vn-ja">Việt - Nhật</md-option>
                        <md-option value="ja-vn">Nhật - Việt</md-option>
                    </md-select>
                </md-field>
                <input
                    class="searchbar"
                    accept="text/plain"
                    v-model="settings.api.query"
                    :placeholder="settings.api.type == 'vn-ja' ? 'từ điển, tu dien' : 'jisho, 辞書'"
                    @input="search"
                    autofocus/>
                <md-button class="md-icon-button clear" @click="clear">
                    <md-icon>clear</md-icon>
                    <md-tooltip>
                        settings.api.type == 'vn-ja' ? Xoá tìm kiếm
                    </md-tooltip>
                </md-button>
            </label>
        </md-content>
        <div>
            <md-empty-state
                    :md-description="settings.api.type == 'vn-ja' ? 'Bắt đầu tìm kiếm mọi thứ bạn muốn.' : '検索ボックスに入力を開始して、必要なものを全て検索してください。'"
                    md-icon="search"
                    :md-label="settings.api.type == 'vn-ja' ? 'Từ điển' : '辞書'"
                    v-if="settings.api.query === '' && !isTyping"/>
            <md-empty-state
                    :md-description="settings.api.type == 'vn-ja' ? 'Thử lại' : '再試行'"
                    md-icon="clear"
                    :md-label="settings.api.type == 'vn-ja' ? 'Không có kết quả!' : '検索結果はありません！'"
                    v-if="settings.api.query !== '' && !hasResults && !isTyping && !isSearching"/>
            <md-progress-spinner
                    md-mode="indeterminate"
                    v-if="isSearching"/>
            <div class="content">
                <slot/>
            </div>
        </div>
    </div>
</template>

<script>
    import debounce from "lodash.debounce";

    export default {
        name: "Search",
        components: {},
        props: {
            label: {
                type: String,
                default: "日本, Japan"
            },
            isSearching: {
                type: Boolean,
                default: false
            },
            hasResults: {
                type: Boolean,
                default: false
            }
        },

        data: () => ({
            isTyping: false,
            filtersExtended: false,
            settings: {
                api: {
                    query: "",
                    type: "vn-ja"
                },
                filters: {}
            }
        }),

        methods: {
            clear() {
                if (this.settings.query !== "") {
                    this.$router.push({
                        name: this.$router.currentRoute.name,
                        query: {}
                    });
                    this.settings.query = "";
                }
            },

            typing: debounce(function () {
                if (this.settings.api.query !== '')
                    this.$router.push({
                        name: this.$router.currentRoute.name,
                        query: this.settings.api
                    });
                else
                    this.$router.push('/').catch(() => {
                    });
                this.isTyping = false;
            }, 500),

            search() {
                this.isTyping = true;
                this.typing();
            },

            emit() {
                if (this.$route.query.query !== undefined)
                    this.settings.api.query = this.$route.query.query;
                else
                    this.settings.api.query = '';

                if (this.$route.query.type !== undefined)
                    this.settings.api.type = this.$route.query.type;

                this.$emit("search", this.settings);
            }
        },

        watch: {
            $route() {
                this.emit();
            }
        },

        mounted() {
            this.emit();
            this.$el.getElementsByTagName("input")[2].focus();
        }
    }
</script>

<style scoped lang="scss">
    @import '~vue-material/dist/theme/engine';

    .md-progress-spinner {
        z-index: 0;
        position: absolute;
        margin: 0 calc(50% - 25px);
    }

    .bar {
        margin: 40px auto;
        width: 60%;
        border: 1px solid gray;
        border-radius: 25px;
        position: relative;

        .md-icon {
            padding: 20px;
            vertical-align: sub;
        }

        .clear {
            position: absolute;
            right: -6px;
        }

        #filters {
            margin: 0 5px 5px 5px;
            padding: 0 10px 10px 10px;
            border-radius: 25px;

            .md-divider {
                margin-bottom: 10px;
            }

            #filters-header {
                margin: 0 0 10px 0;
                text-align: center;
            }
        }

        .type {
            width: calc(30% - 40px);
            margin: 0;
            padding: 0;
            min-height: 0;
            display: inline-block;
            text-align: center;
        }

        .searchbar {
            color: inherit;
            outline: none;
            font-size: 20px;
            background: none;
            border: none;
            width: calc(70% - 80px);
        }

        .searchbar:focus {
            outline: none;
        }

        ::placeholder {
            color: inherit;
            font-size: 20px;
        }
    }

    @media screen and (max-width: 768px) {
        div.bar {
            width: 90%;
            .type {
                width: calc(40% - 40px);
            }
            .searchbar {
                width: calc(60% - 80px);
            }
        }
    }
</style>
