const content_to_merge = [docs[i].content, docs[i].notebook_content];
docs[i].content = content_to_merge.join(' ');
