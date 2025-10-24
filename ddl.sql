-- toujia.toujia_user definition

CREATE TABLE `tg_user` (
  `tg_id` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'tg名字',
  `user_name` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'tg用户名',
  `is_delete` varchar(10) CHARACTER SET utf8mb4 DEFAULT '0' COMMENT '0未删除 1已删除',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`tg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


-- toujia.toujia_user_transfer_group definition

CREATE TABLE `user_transfer_group` (
  `id` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `tg_id` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Telegram ID',
  `bot_id` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Bot ID',
  `group_id` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '群组id',
  `group_type` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '1群组 2频道',
  `group_link` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '群组/频道 链接',
  `group_name` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '群组/频道 名字',
  `group_username` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '群组/频道 用户名',
  `owner` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '0无权限发送 1有权限发送',
  `owner_dict` varchar(500) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '权限字典',
  `is_delete` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '0未删除 1已删除',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- toujia.toujia_user_bot definition

CREATE TABLE `user_bot` (
  `id` varchar(100) CHARACTER SET utf8 NOT NULL,
  `tg_id` varchar(100) CHARACTER SET utf8 NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户名字',
  `user_name` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户用户名',
  `bot_token` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '机器人token',
  `bot_name` varchar(200) CHARACTER SET utf8 DEFAULT NULL COMMENT '机器人名字',
  `bot_start_name` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '机器人启动时的名字',
  `bot_username` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '机器人用户名',
  `bot_flag` varchar(100) CHARACTER SET utf8 DEFAULT NULL COMMENT '机器人启动状态 0未启动 1启动',
  `is_delete` varchar(100) CHARACTER SET utf8 DEFAULT '0' COMMENT '0未删除 1删除',
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;