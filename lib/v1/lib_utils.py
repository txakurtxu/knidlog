def html_db_data(s_html, db_data, c_user, c_days):
    user_ids = []
    x = []
    for row in db_data:
        if row[1] not in user_ids:
            user_ids.append(row[1])
            x.append([])
        tmp_user_id = user_ids.index(row[1])

        row = ["" if tmp_x is None else tmp_x for tmp_x in row]

        if len(row[0]) == 0:
            tmp_l = list(row)
            tmp_l[0] = tmp_l[1]
            row = tuple(tmp_l)

        case_ids = [z[0] for z in x[tmp_user_id]]
        if row[3] not in case_ids:
            tmp_case_id = len(case_ids)
            # diag, trans, clinhis
            x[tmp_user_id].append([row[3], "", "", "", row[0].strip().lower()])
        else:
            tmp_case_id = case_ids.index(row[3])

        if row[5].strip() != "[]" and x[tmp_user_id][tmp_case_id][1] == "":
            x[tmp_user_id][tmp_case_id][1] = row[5].strip()

        if row[6].strip() not in ["[]", ""] and x[tmp_user_id][tmp_case_id][2] == "":
            x[tmp_user_id][tmp_case_id][2] = row[6].strip()

        if row[4].strip() != "" and x[tmp_user_id][tmp_case_id][3] == "":
            x[tmp_user_id][tmp_case_id][3] = row[4].strip()

    s_repl = "<!--XXX-->"
    t_repl = ""
    u_repl = "// XXX"
    t_uniq = t_vacu = t_diag = t_micr = 0
    for u in x:
        c_uniq = len(u)
        c_vacu = c_diag = c_micr = 0
        for c in u:
            if c[1] == c[2] == c[3] == "":
                c_vacu += 1
            if c[1] != "":
                c_diag += 1
            if c[2] != "":
                c_micr += 1
        t_uniq += c_uniq
        t_vacu += c_vacu
        t_diag += c_diag
        t_micr += c_micr
        t_repl += "<tr> <th>" + u[0][4][0].upper() + u[0][4][1: ] + "</th> <th>" + str(c_uniq) + "</th> <th>" + str(c_vacu) + "</th> <th>" + str(c_diag) + "</th> <th>" + str(c_micr) + "</th> </tr>"
    t_repl += "<tr> <th>" + "<span style='display: block; text-align: right;'>Total</span>" + "</th> <th>" + str(t_uniq) + "</th> <th>" + str(t_vacu) + "</th> <th>" + str(t_diag) + "</th> <th>" + str(t_micr) + "</th> </tr>"

    return s_html.replace(s_repl, t_repl).replace(u_repl, "var c_user = \"" + c_user +"\", p_days = " + c_days + ";")
