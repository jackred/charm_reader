def save(title, image, folder, cmap='gray'):
    plt.imsave('./%s/%s.png' % (folder, title), image, cmap=cmap)


def save_skill(title, image):
    save(title, image, 'skills')


def save_rarity(title, image):
    save(title, image, 'rarities', None)


def save_value(title, image):
    save(title, image, 'values')


def save_slot(title, image):
    save(title, image, 'slots')


def save_csv(charms, name):
    charms['mix'] = (charms['skill_1'] + ' ' + charms['value_1'] + ' '
                     + charms['skill_2'] + ' ' + charms['value_2']).str.strip()
    charms['slots'] = (charms['slot_1'] + '-' + charms['slot_2']
                       + '-' + charms['slot_3']).str.replace('-0', '').replace('0', '')
    charms = charms[['skill_1', 'value_1', 'skill_2',
                     'value_2', 'mix', 'slots']]
    charms.to_csv(name, index=False)

