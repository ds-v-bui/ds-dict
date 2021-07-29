<template>
    <div v-if="this.$store.getters.getUser === null">
        <md-button class="md-icon-button md-dense" to="" @click="bookmark" disabled>
            <md-icon v-if="!isBookmarked">
                star_border
            </md-icon>
        </md-button>
        <md-tooltip>
            Đăng nhập để sử dụng chức năng này!
        </md-tooltip>
    </div>
    <md-button v-else class="md-icon-button md-dense" to="" @click="bookmark">
        <md-icon v-if="isBookmarked">
            star
        </md-icon>
        <md-icon v-else>
            star_border
        </md-icon>
    </md-button>
</template>
<script>
    export default {
        name: "Bookmark",

        props: {
            id: {
                type: Number
            },
            type: {
                type: Number
            }
        },

        methods: {
            bookmark() {
                if (this.$store.getters.getUser !== null) {
                    if (this.isBookmarked)
                        this.$store.dispatch('removeBookmark', {type: this.type, bookmark: this.id});
                    else
                        this.$store.dispatch('addBookmark', {type: this.type, bookmark: this.id});
                }
            }
        },

        computed: {
            isBookmarked() {
                let bookmarks = this.$store.getters.getUser;
                if (bookmarks === null)
                    return false;

                return bookmarks.bookmarks.words.includes(this.id);
            }
        }
    }
</script>

<style scoped lang="scss">
    div {
        max-width: 40px;
        display: inline-flex;
        float: right;
    }

    button {
        margin: 0;
    }
</style>
