import re


def getFile(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def saveFile(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def startMatch(pattern, text):
    match = re.match(pattern, text, re.I)
    if match is None:
        return False
    return match


class Bookmark:
    def __init__(self):
        self.root_folder = {
            'type': 'folder',
            'name': 'root',
            'children': [],
        }
        self.text = ''
        self.html = ''
        self.mkdn = ''

    def reset(self):
        self.root_folder['children'] = []

    def toListText(self, is_show_link=True):
        tab = ' ' * 4
        self.text = ''
        folder_icon = '📂' if is_show_link else '📁'

        def visit(node, step=0):
            self.text += '%s%s %s\n' % (tab * step, folder_icon,
                                       node['name'])
            for i in node['children']:
                if i['type'] == 'folder':
                    visit(i, step + 1)
                if is_show_link and i['type'] == 'link':
                    self.text += '%s🔗 [%s](%s)\n' % (tab * (step + 1),
                                                    i['name'], i['href'])

        for i in self.root_folder['children']:
            visit(i)
        return self.text

    def toHTML(self):
        tab = '  '
        self.html = '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>\n<H1>Bookmarks</H1>\n'
        folder_start_template = '%s<DT><H3>%s</H3>\n%s<DL><p>\n'
        folder_end_template = '%s</DL><p>\n'
        link_template = '%s<DT><A HREF="%s">%s</A>\n'
        
        def visit(node, step=0):
            if step == 0:
                self.html += '<DL><p>\n'
            else:
                self.html += folder_start_template % (tab*step, node['name'], tab*step)

            for i in node['children']:
                if i['type'] == 'folder':
                    visit(i, step + 1)
                if i['type'] == 'link':
                    self.html += link_template % (tab*(step+1), i['href'], i['name'])

            if step == 0:
                self.html += '</DL><p>\n'
            else:
                self.html += folder_end_template % (tab*step)

        visit(self.root_folder)
        return self.html

    def parseFromHTML(self, html):
        self.reset()

        path = []

        def go():
            if len(path) == 0:
                path.append(self.root_folder)
            else:
                path.append(path[-1]['children'][-1])

        def back():
            if len(path) > 1:
                path.pop()

        def add_link(name, href):
            path[-1]['children'].append({
                'type': 'link',
                'name': name,
                'href': href,
            })

        def add_folder(name):
            path[-1]['children'].append({
                'type': 'folder',
                'name': name,
                'children': [],
            })

        dlp_start = r'<DL><p>'
        dlp_end = r'</DL><p>'

        dta_start = r'<DT><A'
        dta_ctn = r'<DT><A(.*?)>(.*?)</A>'

        dth3_start = r'<DT><H3'
        dth3_ctn = r'<DT><H3(.*?)>(.*?)</H3>'

        dlp_count = 0
        while len(html) > 0:
            trim_len = 1

            #### match start tag ####
            # DLP
            match = startMatch(dlp_start, html)
            if match:
                dlp_count += 1
                trim_len = match.span()[1]
                go()

            # DTH3
            match = startMatch(dth3_start, html)
            if match:
                match = startMatch(dth3_ctn, html)
                trim_len = match.span()[1]
                add_folder(match.group(2).strip())

            # DTA
            match = startMatch(dta_start, html)
            if match:
                match = startMatch(dta_ctn, html)
                trim_len = match.span()[1]
                href, name = match.groups()
                href = re.search(r'HREF="(.*?)"', href.strip()).group(1)
                add_link(name.strip(), href)

            #### match end tag ####
            # DLP
            match = startMatch(dlp_end, html)
            if match:
                dlp_count -= 1
                trim_len = match.span()[1]
                back()

            html = html[trim_len:].strip()

        # assert dlp_count == 0, "dlp_count should be 0."

    def parseFromListText(self, text):
        self.reset()

        folder_pattern = r'(\s*)[📂📁]{1} (.+)'
        link_pattern = r'(\s*)🔗 \[(.+)\]\((.+)\)'

        level2tabs_folders = [{
            'tabs': [-1],
            'folders': [self.root_folder],
        }]
        last_level = 0
        last_tab = -1

        text = text.strip().split('\n')
        while len(text) > 0:
            cur_level = None
            cur_tab = None
            line = text.pop(0)

            # match folder
            match = startMatch(folder_pattern, line)
            if match:
                # calc cur_level
                cur_tab = len(match.group(1))
                if cur_tab == last_tab:
                    cur_level = last_level
                if cur_tab > last_tab:
                    cur_level = last_level + 1
                if cur_tab < last_tab:
                    for i in reversed(range(last_level)):
                        if cur_tab in level2tabs_folders[i]['tabs']:
                            cur_level = i
                            break
                assert cur_level is not None

                # add new_folder to root
                new_folder = {
                    'type': 'folder',
                    'name': match.group(2),
                    'children': [],
                }
                level2tabs_folders[cur_level -1]['folders'][-1]\
                ['children'].append(new_folder)

                # complete level2tabs_folders
                if len(level2tabs_folders) - 1 < cur_level:
                    level2tabs_folders.append({
                        'tabs': [cur_tab],
                        'folders': [new_folder]
                    })
                else:
                    level2tabs_folders[cur_level]['folders'].append(new_folder)
                    level2tabs_folders[cur_level]['tabs'].append(cur_tab)

                last_tab = cur_tab
                last_level = cur_level

            # match link
            match = startMatch(link_pattern, line)
            if match:
                # calc cur_level
                cur_tab = len(match.group(1))
                if cur_tab == last_tab:
                    cur_level = last_level
                if cur_tab > last_tab:
                    cur_level = last_level + 1
                if cur_tab < last_tab:
                    for i in reversed(range(last_level)):
                        if cur_tab in level2tabs_folders[i]['tabs']:
                            cur_level = i
                            break
                assert cur_level is not None

                # add new_link to root
                new_link = {
                    'type': 'link',
                    'name': match.group(2),
                    'href': match.group(3),
                }
                level2tabs_folders[cur_level -1]['folders'][-1]\
                ['children'].append(new_link)

                last_tab = cur_tab
                last_level = cur_level


if __name__ == "__main__":
    # html = getFile('./bc.html')
    # bookmark = Bookmark()
    # bookmark.parseFromHTML(html)
    # saveFile('./dir_bc.txt', bookmark.toListText(False))

    text = getFile("edit_zy.txt")
    bookmark = Bookmark()
    bookmark.parseFromListText(text)
    saveFile('edit_zy.html', bookmark.toHTML())
