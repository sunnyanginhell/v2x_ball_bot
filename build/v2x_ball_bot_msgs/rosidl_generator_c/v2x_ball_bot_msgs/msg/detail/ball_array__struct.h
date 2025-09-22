// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from v2x_ball_bot_msgs:msg/BallArray.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__STRUCT_H_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'balls'
#include "v2x_ball_bot_msgs/msg/detail/ball__struct.h"

/// Struct defined in msg/BallArray in the package v2x_ball_bot_msgs.
/**
  * BallArray.msg
 */
typedef struct v2x_ball_bot_msgs__msg__BallArray
{
  builtin_interfaces__msg__Time stamp;
  v2x_ball_bot_msgs__msg__Ball__Sequence balls;
} v2x_ball_bot_msgs__msg__BallArray;

// Struct for a sequence of v2x_ball_bot_msgs__msg__BallArray.
typedef struct v2x_ball_bot_msgs__msg__BallArray__Sequence
{
  v2x_ball_bot_msgs__msg__BallArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} v2x_ball_bot_msgs__msg__BallArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__STRUCT_H_
