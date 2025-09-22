// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from v2x_ball_bot_msgs:msg/BallArray.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__BUILDER_HPP_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "v2x_ball_bot_msgs/msg/detail/ball_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace v2x_ball_bot_msgs
{

namespace msg
{

namespace builder
{

class Init_BallArray_balls
{
public:
  explicit Init_BallArray_balls(::v2x_ball_bot_msgs::msg::BallArray & msg)
  : msg_(msg)
  {}
  ::v2x_ball_bot_msgs::msg::BallArray balls(::v2x_ball_bot_msgs::msg::BallArray::_balls_type arg)
  {
    msg_.balls = std::move(arg);
    return std::move(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallArray msg_;
};

class Init_BallArray_stamp
{
public:
  Init_BallArray_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BallArray_balls stamp(::v2x_ball_bot_msgs::msg::BallArray::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_BallArray_balls(msg_);
  }

private:
  ::v2x_ball_bot_msgs::msg::BallArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::v2x_ball_bot_msgs::msg::BallArray>()
{
  return v2x_ball_bot_msgs::msg::builder::Init_BallArray_stamp();
}

}  // namespace v2x_ball_bot_msgs

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__BUILDER_HPP_
