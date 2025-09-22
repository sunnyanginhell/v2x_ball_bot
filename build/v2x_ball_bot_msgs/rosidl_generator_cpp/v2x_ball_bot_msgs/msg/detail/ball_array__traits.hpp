// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallArray.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__TRAITS_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "v2x_ball_bot_msgs/msg/detail/ball_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"
// Member 'balls'
#include "v2x_ball_bot_msgs/msg/detail/ball__traits.hpp"

namespace v2x_ball_bot_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const BallArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: balls
  {
    if (msg.balls.size() == 0) {
      out << "balls: []";
    } else {
      out << "balls: [";
      size_t pending_items = msg.balls.size();
      for (auto item : msg.balls) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const BallArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }

  // member: balls
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.balls.size() == 0) {
      out << "balls: []\n";
    } else {
      out << "balls:\n";
      for (auto item : msg.balls) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const BallArray & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace v2x_ball_bot_msgs

namespace rosidl_generator_traits
{

[[deprecated("use v2x_ball_bot_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const v2x_ball_bot_msgs::msg::BallArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  v2x_ball_bot_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use v2x_ball_bot_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const v2x_ball_bot_msgs::msg::BallArray & msg)
{
  return v2x_ball_bot_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<v2x_ball_bot_msgs::msg::BallArray>()
{
  return "v2x_ball_bot_msgs::msg::BallArray";
}

template<>
inline const char * name<v2x_ball_bot_msgs::msg::BallArray>()
{
  return "v2x_ball_bot_msgs/msg/BallArray";
}

template<>
struct has_fixed_size<v2x_ball_bot_msgs::msg::BallArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<v2x_ball_bot_msgs::msg::BallArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<v2x_ball_bot_msgs::msg::BallArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__TRAITS_HPP_
