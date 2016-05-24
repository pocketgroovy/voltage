__author__ = 'carlos.matsumoto', 'yoshi.miyamoto'

from django.conf.urls import patterns, url

from witches import login
import player_story
import views
import admintool.adm_views
import facebook_model
import google
import recipes
import master
import user
import shop
import avatar_items
import mail
from witches.admintool import QAtool
import tutorial
import support

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^environment/', master.environment_html, name='environment_html'),
                       url(r'^get_environment/(\d{1})', master.get_environment, name='get_environment'),
                       # url(r'^login/(\d{1})', views.login, name='login'),
                       url(r'^create_user/(\d{1})', views.create_user, name='create_user'),
                       url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/witches/logout_session/'}),
                       url(r'^logout_session/', views.logout, name='logout'),

                       url(r'^facebook_graph_login/', facebook_model.facebook_graph_login, name='facebook_graph_login'),

                       url(r'^google/(\w*)', google.google_login, name='google_login'),

                       # master tables
                       url(r'^master/(\w*)/(\d{1})', master.get_all_master, name='get_all_master'),

                       # ping
                       url(r'^ping/(\d{1})', master.ping, name='ping'),

                       # log in
                       url(r'^login_html/', login.login_html, name='login_html'),
                       url(r'^login/(\d{1})', login.login_user, name='login'),

                       # shop
                       url(r'^coin/', shop.buy_with_coins_html, name='buy_with_coins_html'),
                       url(r'^buy_with_coins/(\d{1})', shop.buy_with_coins, name='buy_with_coins'),
                       url(r'^stone/', shop.buy_with_stones_html, name='buy_with_stones_html'),
                       url(r'^buy_with_stones/(\d{1})', shop.buy_with_stones, name='buy_with_stones'),
                       url(r'^premium/', shop.buy_inapp_html, name='buy_inapp_html'),
                       url(r'^buy_inapp/(\d{1})', shop.buy_inapp, name='buy_inapp'),
                       url(r'^ticket/', shop.buy_tickets_html, name='buy_tickets_html'),
                       url(r'^buy_tickets/(\d{1})', shop.buy_tickets, name='buy_tickets'),

                       # user
                       url(r'^password/', user.get_password_html, name='get_password_html'),
                       url(r'^get_password/(\d{1})', user.get_password, name='get_password'),
                       url(r'^restore/', user.restore_html, name='restore_html'),
                       url(r'^set_restore_ids/(\d{1})', user.set_restore_ids, name='set_restore_ids'),
                       url(r'^start_restore/(\d{1})', user.start_restore, name='get_restored'),
                       url(r'^use_potion_entry/', user.use_potion_html, name='use_potion_html'),
                       url(r'^use_potion/(\d{1})', user.use_potion, name='use_potion'),
                       url(r'^use_stamina_entry/', user.use_stamina_html, name='use_stamina_html'),
                       url(r'^use_stamina/(\d{1})', user.use_stamina, name='use_stamina'),
                       url(r'^use_ingredient_entry/', user.use_ingredient_html, name='use_ingredient_html'),
                       url(r'^prep_ingredient/(\d{1})', user.prep_ingredient, name='prep_ingredient'),
                       url(r'^player/', user.get_playerstate_html, name='get_playerstate_html'),
                       url(r'^get_playerstate/(\d{1})', user.get_playerstate, name='get_playerstate'),

                       url(r'^use_ingredient/(\d{1})', user.use_ingredient, name='use_ingredient'),
                       url(r'^howtos/', user.howtos_entry, name='howtos_entry'),
                       url(r'^howtos_progress/(\d{1})', user.howtos_progress, name='howtos_progress'),
                       url(r'^input_name_entry/', user.input_name_entry_html, name='input_name_entry_html'),
                       url(r'^input_names/(\d{1})', user.input_names, name='input_names'),
                       url(r'^update_stamina_entry/', user.update_stamina_html, name='update_stamina_html'),
                       url(r'^update_stamina/(\d{1})', user.handle_stamina_regeneration,
                           name='handle_stamina_regeneration'),
                       url(r'^refill_stamina_entry/', user.refill_stamina_html, name='update_stamina_html'),
                       url(r'^refill_stamina/(\d{1})', user.refill_stamina, name='handle_refill_stamina'),

                       url(r'^update_outfit/(\d{1})', user.update_outfit, name='update_outfit'),

                       url(r'^sync_resources_html/', user.sync_resources_html, name='sync_resources_html'),
                       
                       # HACK: Pointing to temporary sync resources to update db with client values
                       url(r'^sync_resources/(\d{1})', user.sync_resources, name='sync_resources'),

                       # tutorial
                       url(r'^tutorial_progress/(\d{1})', tutorial.progress, name='tutorial_progress'),
                       url(r'^finish_tutorial/(\d{1})', tutorial.finish, name='finish_tutorial'),

                       # mail
                       url(r'^mailbox/', mail.get_all_mails_html, name='get_all_mails_html'),
                       url(r'^get_all_mails/(\d{1})', mail.get_all_mails, name='get_all_mails'),
                       url(r'^open_mail/(\d{1})', mail.open_mail, name='open_mail'),
                       url(r'^mail_badge/', mail.mail_badge_html, name='mail_badge_html'),
                       url(r'^get_mail_badge/(\d{1})', mail.get_mail_badge, name='get_mail_badge'),
                       url(r'^check_scene_mail/(\d{1})', mail.check_scene_mail, name='check_scene_mail'),

                       # player story
                       url(r'^start_scene_entry/', player_story.start_scene_entry, name='start_scene_entry'),
                       url(r'^start_scene/(\d{1})', player_story.start_scene, name='start_scene'),
                       url(r'^playerstorystate_entry/', user.playerstorystate_entry_html,
                           name='playerstorystate_entry_html'),
                       url(r'^playerstorystate_affinities/', user.playerstorystate_affinities,
                           name='playerstorystate_affinities'),
                       url(r'^playerstorystate_choices/', user.playerstorystate_choices,
                           name='playerstorystate_choices'),
                       url(r'^update_playerstorystate/(\d{1})', user.update_playerstorystate,
                           name='update_playerstorystate'),
                       url(r'^complete_scene_entry/', player_story.complete_scene_html, name='complete_scene_html'),
                       url(r'^complete_scene_affinities/', player_story.complete_scene_affinities,
                           name='complete_scene_affinities'),
                       url(r'^complete_scene_choices/', player_story.complete_scene_choices,
                           name='complete_scene_choices'),
                       url(r'^complete_scene/(\d{1})', player_story.complete_scene, name='complete_scene'),
                       url(r'^story_reset_inputs/', player_story.story_reset_inputs, name='story_reset_inputs'),
                       url(r'^story_reset/(\d{1})', player_story.story_reset, name='story_reset'),

                       # recipes
                       url(r'^recipe/', recipes.save_recipe_result_html, name='save_recipe_result_html'),
                       url(r'^save_potion_result/(\d{1})', recipes.save_recipe_result, name='save_recipe_result'),

                       # avatar items
                       url(r'^coordinate/', avatar_items.save_coordination_html, name='save_coordination_html'),
                       url(r'^save_coordination_list/', avatar_items.save_coordination_list,
                           name='save_coordination_list'),
                       url(r'^save_coordination/(\d{1})', avatar_items.save_coordination, name='save_coordination'),
                       url(r'^remove_items/', avatar_items.remove_html, name='remove_html'),
                       url(r'^remove_avaitems/', avatar_items.remove_avatar_item_html, name='remove_avatar_item'),
                       url(r'^remove_avatar_item/(\d{1})', avatar_items.remove_avatar_item, name='remove_avatar_item'),
                       url(r'^remove_coord/', avatar_items.remove_coordination_html, name='remove_coordination_html'),
                       url(r'^remove_coordination/(\d{1})', avatar_items.remove_coordination,
                           name='remove_coordination'),
                       url(r'^check_coord_for_removal/(\d{1})', avatar_items.check_coord_for_removal,
                           name='check_coord_for_removal'),
                       url(r'^remove_confirm/(\d{1})', avatar_items.remove_avatar_item, name='remove_confirm'),

                       url(r'^error_report/', support.receive_error_report, name='error_report'),

#-- From here will be removed for prod --
                        # if you update admintool url names, change const.admintool in master.py
                        # it is used in url_switching_middleware
                        # QA tools
                       url(r'^admintool/add_ingredients_inputs/', admintool.QAtool.add_ingredients_inputs, name='add_ingredients_inputs'),
                       url(r'^admintool/add_all_ingredients/(\d{1})', admintool.QAtool.add_all_ingredients, name='add_all_ingredients'),
                       url(r'^admintool/add_potions_inputs/', admintool.QAtool.add_potions_inputs, name='add_potions_inputs'),
                       url(r'^admintool/add_all_potions/(\d{1})', admintool.QAtool.add_all_potions, name='add_all_potions'),
                       url(r'^admintool/add_avatar_inputs/', admintool.QAtool.add_avatar_inputs, name='add_avatar_inputs'),
                       url(r'^admintool/add_all_avatars/(\d{1})', admintool.QAtool.add_all_avatars, name='add_all_avatars'),

                       # ----------------------- ADMIN TOOL ---------------------#

                       url(r'^admintool/$', admintool.adm_views.home, name='home'),
                       url(r'^admintool/admintoolloadmaster/', admintool.adm_views.load_master, name='loadmaster'),
                       url(r'^admintool/admintooldownloadmaster/', admintool.adm_views.download_master, name='downloadmaster'),
                       url(r'^admintool/admintoolparameters/', admintool.adm_views.parameters, name='parameters'),
                       url(r'^admintool/admintooldeliver/', admintool.adm_views.deliver_window, name='deliver_window'),
                       url(r'^admintool/admintool/deliver/', admintool.adm_views.deliver, name='deliver'),

                       url(r'^admintool/admintoolfetchjson/', admintool.adm_views.fetch_player_json, name='fetchjson'),
                       url(r'^admintool/admintooluploadjson/', admintool.adm_views.upload_player_json, name='uploadjson'),
                       
#--To here will be removed for prod --
                       )
